import os
import subprocess
import json
import requests
import argparse
import getpass
username = getpass.getuser()
REPOSITORY_URL = "https://raw.githubusercontent.com/igortara/FAM/refs/heads/main/Packages/"
INSTALLED_PACKAGES_FILE = "installed_packages.txt"
def install_url(package_url):
    print(package_url)
    try:
        response = requests.get(package_url)
        response.raise_for_status()
        package_data = response.json()
        package_name = package_data.get("name")
        if not package_name:
            print("Error: Package name not found in the JSON data.")
            return None
        return package_data
    except requests.RequestException as e:
        print(f"Error fetching package from {package_url}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {package_url}: {e}")
        return None
    except Exception as e:  
        print(f"An unexpected error occurred while installing from {package_url}: {e}")
        return None

    
def install_package(package_name):
    print(package_name)
    package_url = f"{REPOSITORY_URL}{package_name}.json"
    try:
        response = requests.get(package_url)
        response.raise_for_status()
        package_data = response.json()
        package_name = package_data.get("downloadlink")
        if not package_name:
            print("Error: Download link not found in the JSON data.")
            return None
        print(f"Installing package: {package_name}")
        os.startfile(package_name)
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching package {package_name}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for package {package_name}: {e}")
        return None
    except Exception as e:  
        print(f"An unexpected error occurred while installing package {package_name}: {e}")
        return None
    
    


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