import os
import subprocess
from pathlib import Path
import site


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


def create_python_module(build_dir: Path,
                         source_files: list[Path],
                         module_name: str) -> None:

    compile_cmd: str = "g++ -c {source_file:s} -o {object_file:s} -std=c++2b -I /usr/include/python3.12 -pedantic-errors -Wall -Wextra -Weffc++ -Wconversion -Wsign-conversion"  # noqa: E501
    link_cmd: str = "g++ {object_files:s} -fPIC -shared -o {python_module:s}"

    if (not build_dir.exists()):
        build_dir.mkdir()

    obj_file: Path
    obj_files: list[Path] = []

    for src_file in source_files:

        obj_file = build_dir/f"{src_file.name:s}.o"
        run_shell_command(f"Compile {src_file.name:s}",
                          compile_cmd.format(source_file=str(src_file),
                                             object_file=str(obj_file)))
        obj_files.append(obj_file)

    run_shell_command("Dynamically Link into {module_name:s} module",
                      link_cmd.format(object_files=" ".join([str(file) for file in obj_files]),
                                      python_module=str(Path(site.getsitepackages()[0])/f"{module_name:s}.so")))

    for file in obj_files:
        file.unlink()

    build_dir.rmdir()


if (__name__ == "__main__"):

    src_dir: Path = Path(os.getcwd())/"src"
    src_files: list[Path] = \
        [src_dir/"orig_algo_impl"/"Rasterization.cpp",
         src_dir/"python_bindings"/"Rasterizationmodule.cpp"]

    create_python_module(Path(os.getcwd())/"build",
                         src_files,
                         "Rasterization")
