#!/usr/bin/env python
import argparse
from package import Package, DependentPackageFoundError


def parse_arguments():
    parser = argparse.ArgumentParser(prog='package_manager.py')
    parser.add_argument('-f', type=argparse.FileType('r'), help='Input File', required=True)
    parser.add_argument('-o', type=argparse.FileType('r'), help='Output File (If not specified, stdout will be used)')

    _args = parser.parse_args()
    return _args


def register_package(package_name: str):
    if package_name not in packages:
        packages[package_name] = Package(package_name)


def install(package_name: str):
    register_package(package_name)
    packages[package_name].install(explicitly_installed=True)


def depend(main_package_name: str, *dependent_package_names: [str]):
    register_package(main_package_name)
    for dependent_package_name in dependent_package_names:
        register_package(dependent_package_name)
        packages[main_package_name].depends_on(packages[dependent_package_name])


def remove(package_name: str):
    register_package(package_name)
    try:
        packages[package_name].remove()
    except DependentPackageFoundError as exc:
        print(exc)


def list_packages():
    for package in packages.values():
        if package.installed:
            print(f"         {package.name}")


def process_command(command, *args):
    if command == 'DEPEND':
        depend(args[0], *args[1:])
    elif command == 'INSTALL':
        assert len(args) == 1, "Invalid amount of packages required to install"
        install(args[0])
    elif command == 'LIST':
        assert len(args) == 0, "LIST requires no arguments"
        list_packages()
    elif command == 'REMOVE':
        assert len(args) == 1, "Invalid amount of packages required to install"
        remove(args[0])
    elif command == 'END':
        exit(0)


if __name__ == '__main__':
    args = parse_arguments()

    packages = {}

    for command in args.f.readlines():
        command = command.strip()
        print(command)
        process_command(*command.split(" "))
