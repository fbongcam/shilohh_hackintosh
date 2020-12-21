import os
import requests
import subprocess
import zipfile

download_dir = os.getcwd()


# Downloader
def download_script(json_url, api):
    request = requests.get(json_url)
    json_data = request.json()
    if api == "github":
        filename = json_data["assets"][1]["name"]
        file_url = json_data["assets"][1]["browser_download_url"]
        file = requests.get(file_url, stream=True)
    elif api == "bitbucket":
        filename = json_data["values"][0]["name"]
        file_url = json_data["values"][0]["links"]["self"]["href"]
        file = requests.get(file_url, stream=True)
    print(filename)
    print(file)

    # Download and Write file
    with open(filename, 'wb') as f:
        for chunk in file.iter_content(chunk_size=1024):
            f.write(chunk)


# .kexts to download
#
# 1. WhateverGreen
# 2. Lilu
# 3. AppleALC
# 4. Codec Commander
# 5. FakeSMC
# 6. GenericUSBXHCI
# 7. IntelMausiEthernet
# 8. BrcmPatchRAM

kexts = [
    "https://api.github.com/repos/acidanthera/WhateverGreen/releases/latest",
    "https://api.github.com/repos/acidanthera/Lilu/releases/latest",
    "https://api.github.com/repos/acidanthera/AppleALC/releases/latest",
    "https://api.bitbucket.org/2.0/repositories/RehabMan/" +
    "os-x-eapd-codec-commander/downloads/",
    "https://api.bitbucket.org/2.0/repositories/RehabMan/" +
    "os-x-fakesmc-kozlek/downloads/",
    "https://api.bitbucket.org/2.0/repositories/RehabMan/" +
    "os-x-generic-usb3/downloads/",
    "https://api.bitbucket.org/2.0/repositories/RehabMan/" +
    "os-x-intel-network/downloads/",
    "https://api.github.com/repos/acidanthera/BrcmPatchRAM/releases/latest"
]

# bootloaders
#
# OpenCore
# Clover Bootloader
bootloaders = [
    "https://api.github.com/repos/" +
    "acidanthera/OpenCorePkg/releases/latest",
    "https://api.github.com/repos/" +
    "CloverHackyColor/CloverBootloader/releases/latest"
]

# ACPI files
#


# ssdtPRGen.sh
#
subprocess.call(
    " curl --url " +
    "https://raw.githubusercontent.com/" +
    "Piker-Alpha/ssdtPRGen.sh/Beta/ssdtPRGen.sh --output ssdtPRGen.sh",
    shell=True
    )


def start_download(list):
    list_length = len(list)
    i = 0
    for url in list:
        api = None
        if "github" in url:
            api = "github"
        elif "bitbucket" in url:
            api = "bitbucket"
        download_script(url, api)
        i = i + 1
        if i == list_length - 1:
            start_download(bootloaders)


start_download(kexts)
