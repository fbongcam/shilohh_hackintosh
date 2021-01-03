import os
from os import path
import shutil
import requests
import subprocess
import zipfile
from zipfile import ZipFile


class textstyle:
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


# .kexts
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
    "os-x-fakesmc-kozlek/downloads/",
    "https://api.bitbucket.org/2.0/repositories/RehabMan/" +
    "os-x-generic-usb3/downloads/",
    "https://api.github.com/repos/acidanthera/BrcmPatchRAM/releases/latest",
    "https://api.github.com/repos/acidanthera/IntelMausi/releases/latest"
]

# ACPI files
#
# R4BE
# R4E
acpi = [
    "https://raw.githubusercontent.com/" +
    "fbongcam/shilohh_hackintosh/main/R4E.zip",
    "https://raw.githubusercontent.com/" +
    "fbongcam/shilohh_hackintosh/main/R4BE.zip"
]

# Bootloaders
#
# OpenCore
# Clover Bootloader
bootloaders = [
    "https://api.github.com/repos/" +
    "acidanthera/OpenCorePkg/releases/latest",
    "https://api.github.com/repos/" +
    "CloverHackyColor/CloverBootloader/releases/latest"
]

# Set working directory
download_dir = os.getcwd()


# Filter brcm files according to macOS version
def filter_brcm(os_version, files_in_zip):
    brcm = ["BrcmFirmwareRepo"]
    if os_version == "10.10":
        brcm.extend([
            "BrcmPatchRAM2",
            "BrcmNonPatchRAM2",
            "BrcmPatchRAM3",
            "BrcmBluetoothInjector"])
    elif os_version == "10.11":
        brcm.extend([
            "BrcmPatchRAM.kext",
            "BrcmNonPatchRAM.kext",
            "BrcmPatchRAM3",
            "BrcmBluetoothInjector"])
    elif os_version == "10.15":
        brcm.extend([
            "BrcmPatchRAM.kext",
            "BrcmPatchRAM2",
            "BrcmNonPatchRAM.kext"])
    # Check if list available
    if isinstance(files_in_zip, list):
        files_to_exclude = []
        for item in brcm:
            for file in files_in_zip:
                if item in file:
                    files_to_exclude.append(file)
        files_a = set(files_in_zip)
        files_b = set(files_to_exclude)
        return list(files_a - files_b)


def downloader(filename, file_url):
    file = requests.get(file_url, stream=True, timeout=5)
    print(
        textstyle.BOLD + u"\N{HEAVY CHECK MARK}" +
        textstyle.END + "\t" + filename)
    # Download and Write file
    with open(filename, 'wb') as f:
        for chunk in file.iter_content(chunk_size=32):
            f.write(chunk)


# Get github latest release url for kexts
def github_latest_release_url(url, bt_adapter):
    if "BrcmPatchRAM" in url:
        if bt_adapter is False:
            return False
    request = requests.get(url)
    json_data = request.json()
    if "github" in url:
        filename = json_data["assets"][1]["name"]
        file_url = json_data["assets"][1]["browser_download_url"]
        if "IntelMausi" in url:
            # Check if IntelMausiEthernet.kext is updated
            if "1.0.4" in filename:
                # If not updated, get provided one
                subprocess.call(
                    "curl -s --url " +
                    "https://raw.githubusercontent.com/" +
                    "fbongcam/shilohh_hackintosh/" +
                    "main/IntelMausiEthernet.kext.zip" +
                    " --output IntelMausiEthernet.kext.zip",
                    shell=True
                    )
                print(
                    textstyle.BOLD + u"\N{HEAVY CHECK MARK}" +
                    textstyle.END + "\t" + "IntelMausiEthernet.kext.zip"
                )
                filename = None
                file_url = None
    elif "bitbucket" in url:
        filename = json_data["values"][0]["name"]
        file_url = json_data["values"][0]["links"]["self"]["href"]
    if filename is not None and file_url is not None:
        downloader(filename, file_url)
        if "OpenCore" in filename:
            return json_data["tag_name"]


# Set motherboard
#
print("\nWhich motherboard are you using?")
print(
    "[" + textstyle.BOLD + "1" + textstyle.END + "]\t" +
    "Rampage IV Extreme (R4E)")
print(
    "[" + textstyle.BOLD + "2" + textstyle.END + "]\t" +
    "Rampage IV Black Edition (R4BE)")

mb_type = None

while mb_type is None:
    set_mb = raw_input("type 1 or 2:\t")
    if set_mb == "1":
        mb_type = "R4E"
        print(
            "\nDo you need " + textstyle.BOLD + "bluetooth " +
            textstyle.END + "(bluetooth adapter) support?")
        bt_adapter = None
        while bt_adapter is None:
            set_bt_adapter = raw_input("(y/n):\t")
            if set_bt_adapter == "y":
                bt_adapter = True
                break
            elif set_bt_adapter == "n":
                bt_adapter = False
                break
        break
    elif set_mb == "2":
        mb_type = "R4BE"
        bt_adapter = True
        break

# Set macOS version
#
print("\nWhich macOS version do you need files for?")
print(
    "[" + textstyle.BOLD + "1" + textstyle.END + "]\t" +
    "10.10 or earlier")
print(
    "[" + textstyle.BOLD + "2" + textstyle.END + "]\t" +
    "10.11 - 10.14")
print(
    "[" + textstyle.BOLD + "3" + textstyle.END + "]\t" +
    "10.15 or later")

os_version = None

while os_version is None:
    set_os = raw_input("type 1, 2 or 3:\t")
    if set_os == "1":
        os_version = "10.10"
        break
    elif set_os == "2":
        os_version = "10.11"
        break
    elif set_os == "3":
        os_version = "10.15"
        break

# Ask for bootloader
#
print("\nDo you want to include a Bootloader?")

bootloader = None

while bootloader is None:
    ask_bootloader = raw_input("(y/n):\t")
    # Set bootloader
    if ask_bootloader == "y":
        bootloader = True
        # Ask which bootloader
        print("\nWhich bootloader do you want to use?")
        print(
            "[" + textstyle.BOLD + "1" + textstyle.END + "]\t" +
            "OpenCore")
        print(
            "[" + textstyle.BOLD + "2" + textstyle.END + "]\t" +
            "Clover Bootloader")

        b_type = None

        while b_type is None:
            set_b = raw_input("type 1 or 2:\t")
            if set_b == "1":
                b_type = "OpenCore"
                break
            elif set_b == "2":
                b_type = "Clover"
                break
        break
    elif ask_bootloader == "n":
        break

# Clear terminal window
os.system("clear")
print(textstyle.BOLD + "\nDownloading files..." + textstyle.END)

# Download HFS-Driver
#
subprocess.call(
    "curl -s --url " +
    "https://raw.githubusercontent.com/" +
    "fbongcam/shilohh_hackintosh/main/HFSPlus-64.efi --output HFSPlus-64.efi",
    shell=True
    )
print(
    "\n" +
    textstyle.BOLD + u"\N{HEAVY CHECK MARK}" +
    textstyle.END + "\t" + "HFS-Driver"
)

# Download ACPI files for motherboard
if mb_type == "R4E":
    subprocess.call(
        "curl -s --url " + acpi[0] + " --output R4E.zip",
        shell=True
        )
elif mb_type == "R4BE":
    subprocess.call(
        "curl -s --url " + acpi[1] + " --output R4BE.zip",
        shell=True
        )
print(
    textstyle.BOLD + u"\N{HEAVY CHECK MARK}" +
    textstyle.END + "\t" + "ACPI files"
)

# Download bootloader
if ask_bootloader == "y":
    if b_type == "OpenCore":
        opencore_version = github_latest_release_url(
            bootloaders[0], bt_adapter)
    elif b_type == "Clover":
        github_latest_release_url(bootloaders[1], bt_adapter)

# Download kexts
for url in kexts:
    github_latest_release_url(url, bt_adapter)


# Download ssdtPRGen.sh
#
subprocess.call(
    "curl -s --url " +
    "https://raw.githubusercontent.com/" +
    "Piker-Alpha/ssdtPRGen.sh/Beta/ssdtPRGen.sh --output ssdtPRGen.sh",
    shell=True
    )
print(
    textstyle.BOLD + u"\N{HEAVY CHECK MARK}" +
    textstyle.END + "\t" + "ssdtPRGen.sh"
)

# Create folder kexts
kexts_folder = "kexts"
if path.exists(os.path.join(download_dir, kexts_folder)):
    int = 1
    while True:
        kexts_folder = "kexts" + "(" + str(int) + ")"
        if path.exists(os.path.join(download_dir, kexts_folder)):
            int += 1
            continue
        else:
            os.mkdir(kexts_folder)
            break
else:
    os.mkdir(kexts_folder)


# Extract zip files
print("\nExtracting files...")
for f in os.listdir(download_dir):
    if not f.startswith('.'):
        if zipfile.is_zipfile(f):
            with ZipFile(f, 'r') as zip:
                files_in_zip = zip.namelist()
                if "OpenCore" in f:
                    if not path.exists(os.path.join(
                        download_dir, "OpenCore-{}".format(
                            opencore_version))):
                        os.mkdir("OpenCore-{}".format(opencore_version))
                        zip.extractall(
                            os.path.join(
                                download_dir, "OpenCore-{}".format(
                                    opencore_version)))
                elif mb_type in f:
                    zip.extractall()
                else:
                    if "Brcm" in f:
                        # Filter Brcm files
                        files_in_zip = filter_brcm(os_version, files_in_zip)
                    enumerated_list = list(enumerate(files_in_zip))
                    for index, file in enumerated_list:
                        if "Debug" not in file:
                            if ".kext/" in file:
                                zip.extract(
                                    file,
                                    os.path.join(download_dir, kexts_folder))
                # Delete archive
                os.remove(f)

# Move files out of folders
print("Organizing files...")
for file in os.listdir(os.path.join(download_dir, kexts_folder)):
    if ".kext" not in file:
        dir_path = os.path.join(download_dir, kexts_folder, file)
        for kext_files in os.listdir(dir_path):
            abspath = os.path.abspath(os.path.join(
                download_dir, kexts_folder, file, kext_files))
            shutil.move(abspath, abspath.replace(file, ""))
        # Remove empty folders
        os.rmdir(dir_path)

# Make extracted kexts executable
print("Making files executable...")
if os.path.join(download_dir, "HFSPlus-64.efi"):
    os.chmod(os.path.join(download_dir, "HFSPlus-64.efi"), 0o775)
for f in os.listdir(os.path.join(download_dir, kexts_folder)):
    if ".kext" in f:
        if "FakeSMC_" in f:
            os.chmod(os.path.join(
                download_dir, kexts_folder, f,
                "Contents/MacOS",
                f.replace(".kext", "").replace("FakeSMC_", "")), 0o775)
        else:
            os.chmod(os.path.join(
                download_dir, kexts_folder, f,
                "Contents/MacOS", f.replace(".kext", "")), 0o775)


print(textstyle.BOLD + "\nDone!\n" + textstyle.END)

# Print end information
if bootloader is not None:
    if b_type == "OpenCore":
        print(
            "For OpenCore installation instructions, visit: " +
            textstyle.RED +
            "https://dortania.github.io/OpenCore-Install-Guide/" +
            "installer-guide/opencore-efi.html\n" +
            textstyle.END)
