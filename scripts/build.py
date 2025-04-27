import os
import sys
import copy
import site
import shutil
import argparse
import subprocess
from pathlib import Path
from enum import StrEnum, IntEnum


def mapping_to_string(mapping_title: str,
                      mapping: dict[str, str]) -> str:

    max_key_length: int = max([len(key) for key in mapping])
    return f'\n{mapping_title:s}:\n{'':{'-':s}>{len(mapping_title) + 1:d}s}\n{'\n'.join([f'  {key:>{max_key_length:d}s}: {value:s}' for key, value in mapping.items()]):s}\n'  # noqa: E231, E501


def run_shell_command(description: str,
                      command: str,
                      shell_path: Path = Path.cwd(),
                      successful_return_code: int = 0) -> None:

    shell_results: subprocess.CompletedProcess[bytes] = \
        subprocess.run(command,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       cwd=shell_path,
                       shell=True)

    command_results: dict[str, str] = \
        {'Directory': str(shell_path),
           'command': command}             # noqa: E127

    if shell_results.stdout:
        command_results['Output'] = f'\n\n{'\n'.join([f'{line:s}' for line in shell_results.stdout.decode('utf-8').split('\n')]):s}'  # noqa: E501

    if shell_results.stderr:
        command_results['Error'] = f'\n\n{'\n'.join([f'{line:s}' for line in shell_results.stderr.decode('utf-8').split('\n')]):s}'  # noqa: E501

    printable_shell_results: str = \
        mapping_to_string(description,
                          command_results)

    if shell_results.returncode == successful_return_code:
        print(printable_shell_results)
    else:
        raise Exception(f'\n{printable_shell_results:s}')


class Optimization(IntEnum):

    NONE = 0
    SOME = 1
    RECOMMENDED = 2
    AGGRESSIVE = 3


class Batch:

    _cpp_versions = ["0x", "1y", "1z", "2a", "2b"]

    def __init__(self, src_dir: Path):

        self._src_dir = src_dir
        self._include_dirs: set[Path] = set() 
        self._preprocessor_macros: dict[str, str | None] = {}
        self._library_names: set[Path] = set()
        self._warnings_to_suppress: list[str] = []

        self.set_version_year(2023)
        self.enable_low_level_assembly_debugging(False)
        self.set_optimization_level(Optimization.RECOMMENDED)
        self.remove_assert_statements(True)
        self.disable_compiler_extensions(True)
        self.enable_position_independence(False)
        self.treat_warnings_as_errors(True)
        self.warn_about_questionable_coding_practices(True)
        self.warn_about_some_extra_questionable_coding_practices(True)
        self.warn_about_not_following_effective_cpp_guidelines(True) 
        self.warn_about_implicit_value_changing_conversions(True)
        self.warn_about_implicit_integer_sign_change_conversions(True)

    @property
    def src_dir(self) -> Path:
     
       return self._src_dir

    def add_include_directory(self, directory: Path) -> None:

        self._include_dirs.add(directory)

    def remove_include_directory(self, directory: Path) -> None:

        self._include_dirs.discard(directory)

    def add_preprocessor_macro(self, macro: str, value: str | None) -> None:

        if macro not in self._preprocessor_macros:
            self._preprocessor_macros |= {macro: value}
        else:
            raise Exception("{macro:s} is already a preprocessor macro")

    def change_preprocessor_macro_value(self, macro: str, new_value: str | None) -> None:

        if macro in self._preprocessor_macros:
            self._preprocessor_macros.update(macro, new_value)
        else:
            raise Exception("{macro:s} is not a known preprocessor macro")

    def remove_preprocessor_macro(self, macro: str) -> None:

        if macro in self._preprocessor_macros:
            del self._preprocessor_macros[macro]
        else:
            raise Exception("{macro:s} is not a known preprocessor macro")

    def add_library_name(self, library_name: str) -> None:

        self._library_names.add(library_name)

    def remove_library_name(self, library_name: str) -> None:

        self._library_names.discard(library_name)

    def yield_library_names(self) -> set[Path]:

        return copy.deepcopy(self._library_names)

    def set_version_year(self, version_year: int) -> None:

        if ((version_year - 2011 < 0) and ((version_year - 2011) % 3 != 0)):
            raise ValueError("{version_year:4d} is not a valid version of C++")

        self._version_year = version_year

    def enable_low_level_assembly_debugging(self, decision: bool) -> None:

        if hasattr(self, "_remove_asserts"):
            if self._remove_asserts and decision:
                print("Warning: removing assert statements is not recommended when low-level assembly debugging is enabled")

        if hasattr(self, "_optimization_level"):
            if self._optimization_level is not Optimization.NONE and decision:
                print("Warning: enabling optimizations will result in discrepancies between assembly code and C\\C++ source code.")

        self._assembly_debugging = decision

    def set_optimization_level(self, level: Optimization) -> None:

        if hasattr(self, "_assembly_debugging"):
            if self._assembly_debugging and level is not Optimization.NONE:
                print("Warning: enabling optimizations will result in discrepancies between assembly code and C\\C++ source code.")

        self._optimization_level = level

    def remove_assert_statements(self, decision: bool) -> None:
 
        if hasattr(self, "_assembly_debbugging"):
            if self._assembly_debugging and decision:
                print("Warning: removing assert statements is not recommended when low-level assembly debugging is enabled")       

        self._remove_asserts = decision

    def enable_position_independence(self, decision: bool) -> None:

        self._position_independence = decision

    def treat_warnings_as_errors(self, decision: bool) -> None:

        self._warnings_as_errors = decision

    def warn_about_questionable_coding_practices(self, decision: bool) -> None:
        
        self._warn_about_questionable_coding_practices = decision

    def warn_about_some_extra_questionable_coding_practices(self, decision: bool) -> None:

        self._warn_about_some_extra_questionable_coding_practices = decision

    def warn_about_not_following_effective_cpp_guidelines(self, decision: bool) -> None:

        self._warn_about_not_following_effective_cpp_guidelines = decision

    def warn_about_implicit_value_changing_conversions(self, decision: bool) -> None:

        self._warn_about_implicit_value_changing_conversions = decision

    def warn_about_implicit_integer_sign_change_conversions(self, decision: bool) -> None:

        self._warn_about_implicit_integer_sign_change_conversions = decision

    def suppress_specific_warning(self, warning: str) -> None: 

        self._warnings_to_suppress.append(warning)

    def disable_compiler_extensions(self, decision: bool) -> None:

        self._disable_compiler_extensions = decision

    def _yield_formatted_flags(self) -> str:

        general_compilation_template: str = "g++ -c {{source_file:s}} -o {{object_file:s}} {flags:s}"

        main_decisions: dict[str, str | None] = \
            {                           "std" : f"c++{self.__class__._cpp_versions[int((self._version_year - 2011)/3)]:2s}",
             f"O{self._optimization_level:d}" : None}

        if self._disable_compiler_extensions:
            main_decisions |= {"pedantic-errors" : None}

        if self._assembly_debugging:
            main_decisions |= {"ggdb" : None}

        if self._position_independence:
            main_decisions |= {"fPIC" : None}

        preprocessor_macros: dict[str, str | None] = copy.deepcopy(self._preprocessor_macros)

        if self._remove_asserts:
            preprocessor_macros |= {"NDEBUG": None}

        warnings: list[str] = []

        if self._warnings_as_errors:
            warnings.append("error")

        if self._warn_about_questionable_coding_practices:
            warnings.append("all")

        if self._warn_about_some_extra_questionable_coding_practices:
            warnings.append("extra")

        if self._warn_about_not_following_effective_cpp_guidelines:
            warnings.append("effc++")

        if self._warn_about_implicit_value_changing_conversions:
            warnings.append("conversion")

        if self._warn_about_implicit_integer_sign_change_conversions:
            warnings.append("sign-conversion")

        if self._warnings_to_suppress:
            for warning in self._warnings_to_suppress:
                warnings.append(f"no-{warning:s}")

        flags: list[str] = \
            [f"{flag:s}={value:s}" if value is not None else f"{flag:s}" for flag, value in main_decisions.items()] + \
            [f"D{macro:s}=\\\"{value:s}\\\"" if value is not None else f"D{macro:s}" for macro, value in preprocessor_macros.items()] + \
            [f"I {str(include_dir):s}" for include_dir in self._include_dirs] + \
            [f"W{flag:s}" for flag in warnings]

        return " ".join([f"-{flag:s}" for flag in flags])

    def compile(self, build_dir: Path) -> list[Path]:

        general_compilation_template: str = "g++ -c {{source_file:s}} -o {{object_file:s}} {flags:s}"

        compilation_template: str = \
            general_compilation_template.format(flags=self._yield_formatted_flags())

        abs_obj_file: Path
        abs_obj_files: list[Path] = []
        common_dir: Path = Path(os.path.commonpath([self._src_dir, build_dir]))

        for rel_root, _, rel_src_files in self._src_dir.relative_to(common_dir).walk():
           for rel_src_file in [rel_root/file for file in rel_src_files]:
               if rel_src_file.suffix == ".cpp":

                   abs_obj_file = (build_dir/rel_src_file.name).with_suffix(".o")
                   abs_obj_files.append(abs_obj_file) 

                   run_shell_command(f"Compile {rel_src_file.name:s}",
                                     compilation_template.format(source_file=str(rel_src_file),
                                                                 object_file=str(abs_obj_file.relative_to(common_dir))),
                                    shell_path=common_dir)

        return abs_obj_files


class Builder:

    class _Linking_Templates(StrEnum):

        EXECUTABLE = "g++ {{object_files:s}} -o {executable:s}.exe {{library_names:s}}"
        PYTHON = "g++ {{object_files:s}} -shared -o {dynamic_library:s}.so {{library_names:s}}"

    class _End_Product(StrEnum):

        EXECUTABLE = "exe"
        PYTHON = "py"

    def __init__(self,
                 build_dir: Path,
                 end_product_name: str):

        self._batches: list[Batch] = []

        self._build_dir = build_dir
        self._end_product_name = end_product_name

        if not self._build_dir.exists():
            self._build_dir.mkdir()

    def _compile(self,
                 template_description: str,
                 template: str) -> None:

        abs_obj_files: list[Path] = [abs_obj_file for batch in self._batches for abs_obj_file in batch.compile(self._build_dir)]   

        unique_library_names: set[Path] = set.union(*[batch.yield_library_names() for batch in self._batches]) 

        formatted_library_names: str = " ".join([f"-l{library_name:s}" for library_name in unique_library_names])

        run_shell_command(template_description,
                          template.format(object_files=" ".join([str(abs_obj_file.relative_to(self._build_dir)) for abs_obj_file in abs_obj_files]),
                                          library_names=formatted_library_names),
                          shell_path=self._build_dir)

        for abs_obj_file in abs_obj_files:
            abs_obj_file.unlink()

    def _build_executable(self) -> None:

        self._compile("Build Executable",
                      self._Linking_Templates.EXECUTABLE.format(executable=self._end_product_name))

    def _build_python_module(self,
                             py_bindings_dir: Path) -> None:

        pybind_batch: Batch = Batch(py_bindings_dir)
        pybind_batch.add_include_directory(Path("/usr")/"include"/f"python{sys.version_info.major:d}.{sys.version_info.minor:d}")
        pybind_batch.add_preprocessor_macro("LIBRARY_NAME", self._end_product_name)
        pybind_batch.suppress_specific_warning("unused-parameter")

        self._batches.append(pybind_batch)

        for batch in self._batches:
            batch.enable_position_independence(True)

        self._compile(f"Create Python '{self._end_product_name.lower():s}' Module",
                      self._Linking_Templates.PYTHON.format(dynamic_library=self._end_product_name))

        (self._build_dir/"py.typed").touch()

        prototype_wrapper_script: Path
        for root, _, files in py_bindings_dir.walk():
            for file in files:
                prototype_wrapper_script = root/file
                if prototype_wrapper_script.suffix == ".txt":
                    with open(prototype_wrapper_script, "r") as prototype_wrapper_script_IO:
                        with open(self._build_dir/f"{prototype_wrapper_script.stem:s}.py", "a") as wrapper_script_IO:
                            wrapper_script_IO.write(prototype_wrapper_script_IO.read().format(library_name=self._end_product_name))

    def add_batch(self, batch: Batch) -> None:

        self._batches.append(batch)

    def test_executable(self) -> None:

        for batch in self._batches:
            batch.set_optimization_level(Optimization.NONE)
            batch.remove_assert_statements(False)
            batch.enable_low_level_assembly_debugging(True)

        self._build_executable()

        run_shell_command("Run Executable",
                          f"./{self._end_product_name:s}.exe",
                          self._build_dir)

        shutil.rmtree(self._build_dir)

    def install_python_module(self,
                              py_bindings_dir: Path) -> None:

        self._build_python_module(py_bindings_dir)

        module_dir: Path = [tmp_path for tmp_path in [Path(tmp_path) for tmp_path in site.getsitepackages()] if tmp_path.name == "site-packages"][0]/self._end_product_name.lower()  # noqa: E501

        if (module_dir.exists()):
            shutil.rmtree(module_dir)

        shutil.move(self._build_dir, module_dir)

    def cmd(self,
            py_bindings_dir: Path | None) -> None:

        cmd_parser: argparse.ArgumentParser = argparse.ArgumentParser()
        cmd_parser.add_argument("end_product", choices=[end_product.value for end_product in self._End_Product])
        end_product: self._End_Product = self._End_Product(cmd_parser.parse_args().end_product)

        match end_product:
            case self._End_Product.EXECUTABLE:
                main_builder.test_executable()
            case self._End_Product.PYTHON:
                if py_bindings_dir is not None:
                    main_builder.install_python_module(py_bindings_dir)
                else:
                    raise ValueError("Need a directory with Python Bindings in order to build a Python Module")


if (__name__ == "__main__"):

    src_dir: Path = Path.cwd()/"src"

    orig_algo_impl_batch: Path = Batch(src_dir/"orig_algo_impl")
    orig_algo_impl_batch.add_library_name("fmt")

    main_builder: Builder = Builder(Path.cwd()/"build", "Rasterization")
    main_builder.add_batch(orig_algo_impl_batch)
    main_builder.cmd(src_dir/"python_bindings")
 
