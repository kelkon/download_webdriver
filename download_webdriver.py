import os
import platform
import requests
import sys
import zipfile
import tarfile

# urls from:
# https://github.com/SergeyPirogov/webdriver_manager
# ChromeDriver
# GeckoDriver
def download_webdriver(driver, target_path="."):
    valid_drivers = ["chrome", "edge", "gecko", "ie", "opera"]
    if driver.casefold() not in valid_drivers:
        raise Exception("invalid driver")
    
    if not os.path.isdir(target_path):
        raise Exception("target_path is not a directory")
    
    bit = platform.architecture()[0]
    operating_system = platform.system()
    machine = "x86" if "x86".casefold() in platform.machine() else "ARM" # x86 or ARM
    
    if driver.casefold() == "chrome":
        # get latest version number
        response = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
        latest_version = response.content.decode('utf-8')
        
        url_base = "https://chromedriver.storage.googleapis.com"
        if operating_system.casefold() == "Windows".casefold():
            # there are no 64bit version
            url_path = f"/{latest_version}/chromedriver_win32.zip"
        elif operating_system.casefold() == "Darwin".casefold():
            if machine.casefold == "ARM".casefold():
                url_path = f"/{latest_version}/chromedriver_mac_arm64.zip"
            else:
                url_path = f"/{latest_version}/chromedriver_mac64.zip"
        elif operating_system.casefold() == "Linux".casefold():
            url_path = f"/{latest_version}/chromedriver_linux64.zip"
        else:
            raise Exception("unknown operating system")
        
        # download
        local_filename = url_path.split('/')[-1].split('.')[0] + f"_{latest_version}" + ".zip"
        local_path = os.path.join(target_path, local_filename)
        chunk_size = 1024 * 1024 # 1MB
        with requests.get(url_base + url_path, stream=True) as response:
            response.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)

        # extract 
        with zipfile.ZipFile(local_path, 'r') as zip_ref:
            zip_ref.extractall(target_path)
        return "chrome driver is downloaded"
    
    elif driver.casefold() == "gecko":
        # get latest version number
        response = requests.get("https://api.github.com/repos/mozilla/geckodriver/releases/latest")
        latest_version = response.json()["tag_name"]
        
        url_base = "https://github.com/mozilla/geckodriver/releases/download"
        if operating_system.casefold() == "Windows".casefold():
            if machine.casefold() == "ARM".casefold():
                url_path = f"/{latest_version}/geckodriver-{latest_version}-win-aarch64.zip"
            else:
                url_path = f"/{latest_version}/geckodriver-{latest_version}-win32.zip"
        elif operating_system.casefold() == "Darwin".casefold():
            if machine.casefold() == "ARM".casefold():
                url_path = f"/{latest_version}/geckodriver-{latest_version}-macos-aarch64.tar.gz"
            else:
                url_path = f"/{latest_version}/geckodriver-{latest_version}-macos.tar.gz"
        elif operating_system.casefold() == "Linux".casefold():
            if machine.casefold() == "ARM".casefold():
                url_path = f"/{latest_version}/geckodriver-{latest_version}-linux-aarch64.zip"
            else:
                if bit.casefold() == "64bit".casefold():
                    url_path = f"/{latest_version}/geckodriver-{latest_version}-linux64.tar.gz"
                else:
                    url_path = f"/{latest_version}/geckodriver-{latest_version}-linux32.tar.gz"
        else:
            raise Exception("unknown operating system")
        
        # download
        local_filename = url_path.split('/')[-1].split('.')[0] + f"_{latest_version}" + url_path.split('/')[-1]
        local_path = os.path.join(target_path, local_filename)
        chunk_size = 1024 * 1024 # 1MB
        with requests.get(url_base + url_path, stream=True) as response:
            response.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)

        # extract
        file = tarfile.open(local_path)
        file.extractall(target_path)
        file.close()

        return "gecko driver is downloaded"

    return "? is downloaded"
    


if __name__ == "__main__":
    # download_webdriver("chrome")
    download_webdriver("gecko")