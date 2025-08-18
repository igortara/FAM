import os
import subprocess
import json
import requests
import argparse
import getpass
username = getpass.getuser()
GITHUB_API_PACKAGES_URL = "https://api.github.com/repos/igortara/FAM/contents/Packages"
REPOSITORY_URL = "https://raw.githubusercontent.com/igortara/FAM/refs/heads/main/Packages/"
INSTALLED_PACKAGES_FILE = "installed_packages.txt"
def get_all_package_files_from_api():
    print("Fetching package list from GitHub API...")
    try:
        response = requests.get(GITHUB_API_PACKAGES_URL)
        response.raise_for_status()
        contents = response.json()

        package_names = [] 
        for item in contents:
            if item.get("type") == "file" and item.get("name", "").endswith(".json"):
                name_without_extension = item["name"].replace(".json", "")
                package_names.append(name_without_extension)
        return package_names
    except requests.RequestException as e:
        print(f"Error fetching package list from GitHub API: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from GitHub API: {e}")
        print("Please ensure the GitHub API endpoint returns valid JSON.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while fetching package list: {e}")
        return []
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
    elif action == "list":
        packages = get_all_package_files_from_api()
        if packages:
            print("Available packages:")
            for package in packages:
                print(f"- {package}")
        else:
            print("No packages available.")
    

if __name__ == "__main__":
    main()