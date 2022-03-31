# Generic Package Manager
==============================. 
-- Example project for Job Interview at Vintra--

A simple package manager that handles dependencies

Getting Started
------------

In order to use the package manager, a txt file with some input commands should be created.

Those commands should be one of:

| Command Usage               | Description                                                                     |
|-----------------------------|---------------------------------------------------------------------------------|
| DEPEND item1 item2  [item3] | Package item1 depends on package item2 (and  item3 or any additional packages). |
| INSTALL item1               | Installs item1 and any other packages required by item1                         |
| REMOVE item1                | Removes item1 and, if possible, packages required by item1.                     |
| LIST                        | Lists the names of all currently installed packages.                            |
| END                         | Marks the end                                                                   |

Usage
--------

The input file should be introduced as follows:

`python package_manager.py -f [inputfile]`

If desired, an output file can be also specified:

`python package_manager.py -f [inputfile] -o [outputfile]`

Unit testing
--------------

Both `package.py` and `package_manager.py` have unit tests that can be located in `tests`.

In order to execute them, `unittest` would be used as follows:

`python -m unittest tests.[test_file].[test_case].[test]`

For example:

`python -m unittest tests.test_package`

