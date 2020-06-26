from pathlib import Path
import subprocess
import argparse


def make_operation(command: str):
    root = Path(__file__).absolute().parent
    if not Path.joinpath(root, 'build').exists():
        Path.joinpath(root, 'build').mkdir(exist_ok=True)
    for cwe in Path.joinpath(root, 'testcases').rglob('*'):
        if str(cwe).endswith('Makefile'):
            print(f'Makefile found at {cwe}!')
            try:
                subprocess.run(args=['make', command], stderr=subprocess.STDOUT, cwd=str(cwe.parent), check=True)
            except subprocess.CalledProcessError as err:
                print('Status : FAIL', err.returncode)


def delete_bat_files():
    for cwe in Path.joinpath(Path(__file__).absolute().parent, 'testcases').rglob('*'):
        if str(cwe).endswith('.bat'):
            cwe.unlink(missing_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--all', dest='all', action='store_true',
                        help='Iterates over all testcase directories and executes the corresponding '
                             'Makefile with "make all".')
    parser.add_argument('-c', '--clean', dest='clean', action='store_true',
                        help='Iterates over all testcase directories and executes the corresponding '
                             'Makefile with "make clean".')
    parser.add_argument('-rb', '--remove-bat', dest='remove_bat', action='store_true',
                        help='Removes bat files in all testcase directories. As they are not needed'
                             'for this project.')
    args = parser.parse_args()

    if args.all:
        make_operation(command='all')
    if args.clean:
        make_operation(command='clean')
    if args.remove_bat:
        delete_bat_files()
