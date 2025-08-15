import os
import subprocess
import json
import requests
import argparse

INSTALLED_PACKAGES_FILE = "installed_packages.txt"

def install_package(package_name):
    print(package_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", type=str)
    parser.add_argument("package_name", type=str, nargs='?', default=None)
    
    args = parser.parse_args()
    action = args.action.lower()
    package_name = args.package_name

    if action == "install":
        if package_name:
            install_package(package_name)
        else:
            print("Error: no package name provided for installation.")
    

if __name__ == "__main__":
    main()