import sys
import copy
import site
import shutil
import subprocess
from enum import IntEnum
from pathlib import Path


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

    def disable_compiler_extensions(self, decision: bool) -> None:

        self._disable_compiler_extensions = decision

    def _yield_formatted_flags(self) -> str:

        general_compilation_template: str = "g++ -c {{source_file:s}} -o {{object_file:s}} {flags:s}"

        main_decisions: dict[str, str | None] = \
            {                           "std" : f"c++{self.__class__._cpp_versions[int((self._version_year - 2011)/3)]:2s}",
             f"O{self._optimization_level:d}" : None}

        if self._disable_compiler_extensions:
            main_decisions |= {"pedantic-errors" : None}

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

        obj_file: Path
        obj_files: list[Path] = []

        if not build_dir.exists():
            build_dir.mkdir()

        for root, _, src_files in self._src_dir.walk():
           for src_file in [root/file for file in src_files]:
               if src_file.suffix == ".cpp":

                   obj_file = (build_dir/src_file.name).with_suffix(".o")
                   obj_files.append(obj_file) 

                   run_shell_command(f"Compile {src_file.name:s}",
                                     compilation_template.format(source_file=str(src_file),
                                                                 object_file=str(obj_file)))

        return obj_files


class Builder:

    def __init__(self):

        self._batches: list[Batch] = []

    def _compile(self,
                 build_dir: Path,
                 template_description: str,
                 template: str) -> None:

        obj_files: list[Path] = [obj_file for batch in self._batches for obj_file in batch.compile(build_dir)]   

        unique_library_names: set[Path] = set.union(*[batch.yield_library_names() for batch in self._batches]) 

        formatted_library_names: str = " ".join([f"-l{library_name:s}" for library_name in unique_library_names])

        run_shell_command(template_description,
                          template.format(object_files=" ".join([str(file.relative_to(build_dir)) for file in obj_files]),
                                          library_names=formatted_library_names),
                          shell_path=build_dir)

        for file in obj_files:
            file.unlink()

    def add_batch(self, batch: Batch) -> None:

        self._batches.append(batch)

    def build_executable(self,
                         build_dir: Path,
                         executable_name: str) -> None:

        linking_template: str = "g++ {{object_files:s}} -o {executable:s}.exe {{library_names:s}}"

        self._compile(build_dir,
                      "Build Executable",
                      linking_template.format(executable=executable_name))


    def build_python_module(self,
                            library_name: str,
                            module_name: str,
                            py_bindings_dir: Path,
                            prototype_wrapper_scripts: list[Path]) -> None:

        linking_template: str = "g++ {{object_files:s}} -shared -o {current_library:s}.so {{library_names:s}}"

        build_dir: Path = Path("build")

        pybind_batch: Batch = Batch(py_bindings_dir)
        pybind_batch.add_include_directory(Path("/usr")/"include"/f"python{sys.version_info.major:d}.{sys.version_info.minor:d}")
        pybind_batch.add_preprocessor_macro("LIBRARY_NAME", library_name)

        self._batches.append(pybind_batch)

        for batch in self._batches:
            batch.enable_position_independence(True)

        self._compile(build_dir,
                      f"Dynamically Link into {library_name:s} Library",
                      linking_template.format(current_library=library_name))

        tmp_module_dir: Path = build_dir/library_name
        tmp_module_dir.mkdir()

        shutil.move(build_dir/f"{library_name:s}.so", tmp_module_dir)

        (tmp_module_dir/"py.typed").touch()
        for prototype_wrapper_script in prototype_wrapper_scripts:
            with open(prototype_wrapper_script, "r") as prototype_wrapper_script_IO:
                with open(tmp_module_dir/f"{prototype_wrapper_script.stem:s}.py", "a") as wrapper_script_IO:
                    wrapper_script_IO.write(prototype_wrapper_script_IO.read().format(library_name=library_name))

        module_dir: Path = [tmp_path for tmp_path in [Path(tmp_path) for tmp_path in site.getsitepackages()] if tmp_path.name == "site-packages"][0]/module_name  # noqa: E501
        if (module_dir.exists()):
            shutil.rmtree(module_dir)
        shutil.move(tmp_module_dir, module_dir)
        build_dir.rmdir()


def build_and_test_executable(builder: Builder,
                              executable_name: str,
                              library_names: list[str] | None = None) -> None:

    build_dir: Path = Path.cwd()/"build"

    builder.build_executable(build_dir,
                             executable_name)

    run_shell_command("Run Executable",
                      f"./{executable_name:s}.exe",
                      build_dir)

    shutil.rmtree(build_dir)


if (__name__ == "__main__"):

    src_dir: Path = Path("src")

    orig_algo_impl_batch: Path = Batch(src_dir/"orig_algo_impl")
    orig_algo_impl_batch.add_library_name("fmt")

    main_builder: Builder = Builder()
    main_builder.add_batch(orig_algo_impl_batch)

    """
    build_and_test_executable(main_builder,
                              "Rasterization")
    """
    py_bindings_dir: Path = src_dir/"python_bindings"

    main_builder.build_python_module("Rasterization",
                                     "rasterization",
                                     py_bindings_dir,
                                     [py_bindings_dir/"__init__.txt"])
    #"""
