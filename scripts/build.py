import os
import subprocess
from pathlib import Path
import site
import shutil


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


def compile_source_files(source_files: list[Path],
                         build_dir: Path,
                         include_dirs: list[Path] = [],
                         preprocessor_macros: dict[str, str] = {}) -> list[Path]:

    warnings: list[str] = ["all", "extra", "effc++", "conversion", "sign-conversion"]

    language_standard_flags: list[str] = ["std=c++2b"]
    build_configuration_flags: list[str] = ["O2", "DNDEBUG"] 
    include_flags: list[str] = [f"I {str(include_dir):s}" for include_dir in include_dirs]
    warning_flags: list[str] = ["pedantic-errors"] + [f"W{flag:s}" for flag in warnings] 
    preprocessor_flags: list[str] = [f"D{macro:s}=\\\"{value:s}\\\"" for macro, value in preprocessor_macros.items()]

    flags: list[str] = \
        language_standard_flags + \
        build_configuration_flags + \
        include_flags + \
        warning_flags + \
        preprocessor_flags

    compile_cmd: str = "g++ -c {source_file:s} -o {object_file:s} {flags:s}"

    obj_file: Path
    obj_files: list[Path] = []

    for src_file in source_files:

        obj_file = build_dir/f"{src_file.stem:s}.o"

        run_shell_command(f"Compile {src_file.name:s}",
                          compile_cmd.format(source_file=str(src_file),
                                             object_file=str(obj_file),
                                             flags=" ".join([f"-{flag:s}" for flag in flags])))

        obj_files.append(obj_file)

    return obj_files


def link_object_files(object_files: list[Path],
                      build_dir: Path,
                      library_name: str) -> None:

    link_cmd: str = "g++ {object_files:s} -fPIC -shared -o {library:s}"

    run_shell_command(f"Dynamically Link into {library_name:s} module",
                      link_cmd.format(object_files=" ".join([str(file) for file in object_files]),
                                      library=str(build_dir/f"{library_name:s}.so")))

    for file in object_files:
        file.unlink()


def create_python_module(source_files: list[Path],
                         module_files: list[Path],
                         py_wrappers: list[Path],
                         library_name: str) -> None:
 
    build_dir: Path = Path("build")
    if (build_dir.exists()):
        shutil.rmtree(build_dir)
    build_dir.mkdir()

    tmp_module_dir: Path = build_dir/library_name
    tmp_module_dir.mkdir()

    src_obj_files = compile_source_files(source_files, build_dir)

    module_obj_files = \
        compile_source_files(module_files,
                             build_dir,
                             [Path("/usr")/"include"/"python3.12"],
                             {"LIBRARY_NAME": library_name})

    link_object_files(src_obj_files + module_obj_files,
                      tmp_module_dir,
                      library_name)

    (tmp_module_dir/"py.typed").touch()
    for py_wrapper in py_wrappers:
        shutil.copy(py_wrapper, tmp_module_dir/py_wrapper.name)

    module_dir: Path = [tmp_path for tmp_path in [Path(tmp_path) for tmp_path in site.getsitepackages()] if tmp_path.name == "site-packages"][0]/library_name  # noqa: E501
    print(module_dir)
    if (module_dir.exists()):
        shutil.rmtree(module_dir)
    shutil.move(tmp_module_dir, module_dir)

    build_dir.rmdir()


if (__name__ == "__main__"):

    src_dir: Path = Path("src")

    src_files: list[Path] = \
        [src_dir/"orig_algo_impl"/"Rasterization.cpp"]

    mod_files: list[Path] = \
        [src_dir/"python_bindings"/"Rasterizationmodule.cpp"]

    py_wrappers: list[Path] = \
        [src_dir/"python_bindings"/"__init__.py"]

    create_python_module(src_files,
                         mod_files,
                         py_wrappers, 
                         "Rasterization")
