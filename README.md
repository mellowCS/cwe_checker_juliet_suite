# cwe_checker_juliet_suite

## Overview

Contains an altered version of the Juliet Suite v1.3 for C/C++ from Oct. 2017 compatible with Linux.
The difference to the original Juliet Suite lies in how the project is structured, how the testcases are compiled
and where the resulting binaries are stored.

For compatibility with Linux, the *-lpthread* flag has been changed to *-pthread* and generally all Windows specific
testcases are ignored.

## Use

Just clone the repository into some directory:

```
git clone https://github.com/mellowCS/cwe_checker_juliet_suite.git
```

and call **handle_make.py** in the project's root directory with -a or --all:

```
python3 handle_make.py --all
```

to initialise the compilation of all CWEs. Each binary will be stored in a dedicated **build** directory in the root of the project.
**Hint:** You may want to run it in *sudo*.

After everything has been compiled, **handle_make.py** can be called with -c or --clean

```
python3 handle_make.py --clean
```

to remove all *.o and *.out files.

Additionally **handle_make.py** has a -rb or --remove-bat flag which removes all bat files that are
used to run tests in Visual Studio as they are unnecessary

```
python3 handle_make.py --remove-bat
```

## Tests

To run the CWE checker on the test suite, we provide a dedicated script **cwe_checker_test.py** that can be
found in the test folder. It allows to either run all supported CWEs on the test suite using the following command

```
python3 cwe_checker_test.py --all
```

or to only run user specified CWEs on the test suite using the following command and a list of CWEs

```
python3 cwe_checker_test.py --partial CWEXXX CWEYYY
```

If the user is running the CWE checker in a docker container, the docker flag can additionally be added to the command

```
python3 cwe_checker_test.py --all --docker
```

The user can also provide their own config json for the CWE checker by providing the path to the command

```
python3 cwe_checker_test.py --all --config /path/to/config_file
```

## Dev

The Makefiles for all compatible testcases have already been created and lie in their corresponding testcase directories.
However, if changes have to be made to the Makefiles, they should be done via the **create_per_cwe_files.py** which creates
a Makefile for each CWE.

All testcases rely on files in the **testcasesupport** directory which has to be noted when new testfiles are added
to the suite.
1. *std_testcase.h:*
  - included in all testcases
  - contains variable and macro definitions
  - includes std_testcase_io.h and stdio.h
2. *io.c / std_testcase_io.h:*
  - definitions for functions used in testcases
  - global variables for control flow testcases
3. *std_thread.c/.h:*
  - thread-related functions used by testcases
4. *main.cpp:*
  - contains Main function calling all good and bad functions for each test case
  - each CWE and its splits contain their own main.cpp
5. *main_linux.cpp:*
  - contains Main function calling all non-Windows specific functions
6. *testcases.h:*
  - contains declarations of all good and bad functions
  - each CWE and its splits contain their own testcases.h

All further information about the files of the Juliet suite can be found in the official docs contained in the **doc** directory
