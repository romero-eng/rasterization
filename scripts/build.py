import os
import subprocess
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


def create_dynamic_library(src_dir: Path,
                           build_dir: Path,
                           source_files: list[str],
                           library_name: str) -> None:

    obj_file: Path
    obj_files: list[Path] = []

    for file in source_files:

        obj_file = build_dir/f"{file:s}.o"
        run_shell_command(f"Compile {file:s}", f"g++ -c {str(src_dir/file):s}.cpp -o {str(obj_file):s} -std=c++2b -I /usr/include/python3.12 -pedantic-errors -Wall -Wextra -Weffc++ -Wconversion -Wsign-conversion")
        obj_files.append(obj_file)

    obj_files_str = " ".join([str(file) for file in obj_files])
    run_shell_command("Dynamically Link into {library_name:s}.so", f"g++ {obj_files_str:s} -fPIC -shared -o {str(build_dir/library_name):s}.so")

    for file in obj_files:
        file.unlink()


if (__name__=="__main__"):

    build_dir = Path(os.getcwd())/"build"

    if(not build_dir.exists()):
        build_dir.mkdir()

    create_dynamic_library(Path(os.getcwd())/"src",
                           Path(os.getcwd())/"build",
                           ["Rasterization", "Rasterizationmodule"],
                           "Rasterization")

