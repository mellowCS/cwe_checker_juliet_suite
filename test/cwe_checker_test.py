import argparse
import os
import re


class UnknownCweException(Exception):
    pass


known_modules = ['CWE190', 'CWE367', 'CWE415', 'CWE416', 'CWE426', 'CWE457', 'CWE467', 'CWE476', 'CWE676']


def build_bap_cmd(filename: str, target: str) -> list:
    if 'travis' in os.environ['USER']:
        abs_path = os.path.abspath(f'../build/{filename}')
        cmd = f'docker run --rm -v {abs_path}:/tmp/input cwe-checker:latest bap /tmp/input --pass=cwe-checker ' \
              f'--cwe-checker-partial=CWE{target}  --cwe-checker-config=/home/bap/cwe_checker/src/config.json'
    else:
        cmd = f'bap ../build/{filename} --pass=cwe-checker ' \
              f'--cwe-checker-partial=CWE{target} --cwe-checker-config=src/config.json'
    return cmd.split()


def build_bap_emulation_cmd(filename: str) -> list:
    if 'travis' in os.environ['USER']:
        abs_path = os.path.abspath(f'../build/{filename}')
        cmd = f'docker run --rm -v {abs_path}:/tmp/input cwe-checker:latest bap /tmp/input --recipe=recipes/emulation'
    else:
        cmd = f'bap ../build/{filename} --recipe=recipes/emulation'
    return cmd.split()


def get_test_file(cwe: str) -> list:
    pass


def run_cwe_checker_on_test_suite(user_input: argparse.Namespace):
    modules = known_modules if user_input.all else user_input.partial

    for mod in modules:
        files = get_test_file(cwe=mod)
        if mod in ['CWE415', 'CWE416']:
            for file in files:
                build_bap_emulation_cmd(filename=file.rpartition('/')[1])
        else:
            for file in files:
                name = file.rpartition('/')[1]
                cwe_num = re.compile(r'CWE(\d+)(_s\d+)?$')
                target = cwe_num.search(name).group(1)
                build_bap_cmd(filename=name, target=target)


def sanitise_user_input(args):
    if not all(cwe in known_modules for cwe in args.partial):
        raise UnknownCweException(f'\n\nCWE is not supported by either the CWE checker or the juliet test suite.\n'
                                  f'Supported CWEs are: {known_modules}\n')


def get_user_input() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--all', action='store_true', dest='all',
                       help='Run all CWE checks on the juliet test suite.')
    group.add_argument('-p', '--partial', nargs='+', dest='partial',
                       help='Run CWE checks based on passed list CWEXXX CWEYYY ... on the juliet test suite.')
    args = parser.parse_args()

    sanitise_user_input(args=args)

    return args


if __name__ == '__main__':
    run_cwe_checker_on_test_suite(get_user_input())
