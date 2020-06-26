import argparse
import re
import subprocess
from pathlib import Path
from typing import Generator


class UnknownCweException(Exception):
    pass


class InvalidPathException(Exception):
    pass


class InvalidFileTypeException(Exception):
    pass


known_modules = {'CWE190': b'Integer Overflow or Wraparound',
                 'CWE367': b'Time-of-check Time-of-use Race Condition',
                 'CWE415': b'Double Free',
                 'CWE416': b'Use After Free',
                 'CWE426': b'Untrusted Search Path',
                 'CWE457': b'Use of Uninitialized Variable',
                 'CWE467': b'Use of sizeof on a Pointer Type',
                 'CWE476': b'NULL Pointer Dereference',
                 'CWE676': b'Use of Potentially Dangerous Function'}


def is_split(cwe: Path):
    if list(cwe.glob('s*')):
        return True
    return False


def remove_ignored_files(files: list):
    ignored = re.compile(r'^.*(?:(?:w32|wchar_t|good)|(?:main\.cpp|main_linux\.cpp)).*$')
    return [file for file in files if not ignored.match(str(file))]


def count_testcases() -> dict:
    testcase_path = Path(__file__).absolute().parent.parent / 'testcases'
    testcases_per_module = dict()
    for cwe in testcase_path.glob('CWE*'):
        module = str(cwe).rsplit('/')[-1].split('_')[0]
        if module in known_modules.keys():
            if is_split(cwe):
                for split in cwe.glob('s*'):
                    files = remove_ignored_files(list(split.glob('*.c*')))
                    testcases_per_module[module + '_' + str(split).rsplit("/")[-1]] = len(files)
            else:
                files = remove_ignored_files(list(cwe.glob('*.c*')))
                testcases_per_module[module] = len(files)

    return testcases_per_module


def execute_and_check_occurrence(bap_cmd, string):
    occurrence = 0
    output = subprocess.check_output(bap_cmd)
    for line in output.splitlines():
        if string in line:
            occurrence += 1
    return occurrence


def execute_emulation_and_check_occurrence(bap_cmd, string):
    occurrence = 0
    output = subprocess.check_output(bap_cmd)
    for line in output.splitlines():
        if string in line:
            occurrence += 1
    return occurrence


def build_bap_cmd(filename: str, target: str, docker: bool = False, config: str = Path.home() / 'cwe_checker/src/config.json') -> list:
    if docker:
        abs_path = Path.cwd().parent / f'build/{filename}'
        cmd = f'docker run --rm -v {abs_path}:/tmp/input fkiecad/cwe_checker bap /tmp/input --pass=cwe-checker ' \
              f'--cwe-checker-partial=CWE{target}'
    else:
        cmd = f'bap ../build/{filename} --pass=cwe-checker ' \
              f'--cwe-checker-partial=CWE{target} --cwe-checker-config={config}'
    return cmd.split()


def build_bap_emulation_cmd(filename: str, docker: bool = False) -> list:
    recipe_path = Path.home() / 'cwe_checker/recipes/emulation/'
    if docker:
        abs_path = Path.cwd().parent / f'build/{filename}'
        cmd = f'docker run --rm -v {abs_path}:/tmp/input cwe-checker:latest bap /tmp/input --recipe=recipes/emulation'
    else:
        cmd = f'bap ../build/{filename} --recipe={recipe_path}'
    return cmd.split()


def get_test_files(cwe: str) -> Generator[Path, None, None]:
    build_path = Path(__file__).absolute().parent.parent / 'build'
    return build_path.glob(cwe + '*')


def display_results(file: str, detected: int, expected: dict):
    cwe = file.rsplit('/')[-1]
    if expected[cwe] == detected:
        print(f'PASSED: [Test] {cwe}: expected detections: {expected[cwe]}, actual detections: {detected}')
    else:
        print(f'FAILED: [Test] {cwe}: expected detections: {expected[cwe]}, actual detections: {detected}')


def run_cwe_checker_on_test_suite(user_input: argparse.Namespace):
    modules = known_modules.keys() if user_input.all else user_input.partial
    testcases_per_cwe = count_testcases()
    for mod in modules:
        files = get_test_files(cwe=mod)
        if mod in ['CWE415', 'CWE416']:
            for file in files:
                cmd = build_bap_emulation_cmd(filename=str(file).rpartition('/')[2])
                detected = execute_emulation_and_check_occurrence(bap_cmd=cmd, string=known_modules[mod])
                display_results(file=str(file), detected=detected, expected=testcases_per_cwe)
        else:
            for file in files:
                name = str(file).rpartition('/')[2]
                cwe_num = re.compile(r'CWE(\d+)(_s\d+)?$')
                target = cwe_num.search(name).group(1)
                if user_input.config:
                    cmd = build_bap_cmd(filename=name, target=target, docker=user_input.docker, config=user_input.config)
                else:
                    cmd = build_bap_cmd(filename=name, docker=user_input.docker, target=target)
                detected = execute_and_check_occurrence(bap_cmd=cmd, string=known_modules[mod])
                display_results(file=str(file), detected=detected, expected=testcases_per_cwe)


def sanitise_user_input(args: argparse.Namespace):
    if args.partial:
        if not all(cwe in known_modules.keys() for cwe in args.partial):
            raise UnknownCweException(f'\n\nCWE is not supported by either the CWE checker or the juliet test suite.\n'
                                      f'Supported CWEs are: {list(known_modules.keys())}\n')
    if args.config:
        if not Path(args.config).is_file():
            raise InvalidPathException(f'\n\nPath: {args.config} is not a file.\n')
        if not Path(args.config).suffix == '.json':
            raise InvalidFileTypeException(f'\n\nFile: {args.config} is not of type json.\n')


def get_user_input() -> argparse.Namespace:
    parser = argparse.ArgumentParser(epilog=f'Supported CWEs: {list(known_modules.keys())}')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--all', action='store_true', dest='all',
                       help='Run all CWE checks on the juliet test suite.')
    group.add_argument('-p', '--partial', nargs='+', dest='partial',
                       help='Run CWE checks based on passed list CWEXXX CWEYYY ... on the juliet test suite.')
    parser.add_argument('-c', '--config', dest='config', type=str,
                        help='Configuration path for the CWE checker. If not set, it is assumed that '
                             'the CWE checker is stored at /home/user/')
    parser.add_argument('-d', '--docker', action='store_true', dest='docker',
                        help='If set, the CWE checker is run from the docker container and not the local installation. '
                             'Default: False')
    args = parser.parse_args()

    sanitise_user_input(args=args)

    return args


if __name__ == '__main__':
    run_cwe_checker_on_test_suite(get_user_input())
