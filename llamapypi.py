import os

import requests
from bs4 import BeautifulSoup
from colored import back, fore, style
from llama_index import LLM


# Fetch package details
def fetch_package_info(package_name):
    url = f"https://pypi.org/project/{package_name}/"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"{fore.RED}Error: Unable to fetch package information.{style}")
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    description = soup.find("meta", {"name": "description"})["content"]
    version = soup.find("h1").text.split()[-1]
    return {"name": package_name, "description": description, "version": version}


# Fetch all packages from user profile
def fetch_user_packages(username):
    url = f"https://pypi.org/user/{username}/"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"{fore.RED}Error: Unable to fetch user profile.{style}")
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    packages = [a.text for a in soup.find_all("a", {"class": "package-snippet"})]
    return packages


# Process package and save to file
def process_package(package_name):
    info = fetch_package_info(package_name)
    if info:
        print(
            f"{fore.GREEN}Processing package: {info['name']} - {info['version']}{style}"
        )
        llm = LLM()
        processed_info = llm.process(info["description"])
        with open(f"{OUTPUT_DIR}/{info['name']}_info.txt", "w") as f:
            f.write(processed_info)


# Process user profile and packages
def process_user(username):
    packages = fetch_user_packages(username)
    if packages:
        for package in packages:
            process_package(package)


# Main function to start the process
def main():
    url = input(f"{fore.CYAN}Enter PyPI URL (package or user profile): {style}")

    if "user" in url:
        username = url.split("/")[-1]
        print(f"{fore.YELLOW}Processing user profile: {username}{style}")
        process_user(username)
    else:
        package_name = url.split("/")[-1]
        print(f"{fore.YELLOW}Processing package: {package_name}{style}")
        process_package(package_name)


if __name__ == "__main__":
    main()
