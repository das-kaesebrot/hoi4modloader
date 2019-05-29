from pathlib import Path
import os
import re
import string
import platform
import tkinter
from tkinter import filedialog

currentOS = platform.system()

# enable this to override checking for path
overrideDefaultPath = False
# Paste your custom path here if above option is enabled
userDefinedPath = ""

print("### ATTENTION ###")

def setdefaultPath(currentOS):
    path = ""
    print("Detected OS: " + currentOS)
    if currentOS == "Linux":
        path = "~/.local/share/Paradox Interactive/Hearts of Iron IV"
    elif currentOS == "Darwin":
        path = "~/Documents/Paradox Interactive/Hearts of Iron IV"
    elif currentOS == "Windows":
        path = os.path.join(os.path.expandvars("%userprofile%"),"Documents","Paradox Interactive","Hearts of Iron IV")
    else:
        currentOS = "OS not detected"
        path = ""
        print("Unable to detect OS, please point to HOI4 Documents folder manually")
    print("Default path was automatically set to: " + path + "\n")
    
    path2 = Path(path)
    return path2;
    # return path;

# replace this 

if overrideDefaultPath:
    defaultpath = userDefinedPath
    print("Setting path to " + defaultpath)
else:
    defaultpath = setdefaultPath(currentOS)

filename = "settings.txt"
filepath1 = defaultpath / filename

def ReadFileStatus():
    status = ReadFile(filepath1)
    if status:
        labeltext = "File read successfully"
    else:
        labeltext = "Error reading file"

    return;

def printModNames():



    return

def ReadFile(filepath):

    success = False
    
    exists = os.path.isfile(filepath)
    if not exists:
        print("File not found")
        return success;

    readlines = False

    counter = 0

    f = open(filepath, 'r')

    print("Reading settings.txt...")

    modids = []

    for line in f:
        if "last_mods" in line:
            readlines = True
        elif "}" in line and readlines:
            readlines = False
        if ".mod" in line and readlines:
            temp = line
            temp = re.sub("\D", "", temp)
            modids.append(int(temp))
            counter += 1

    print("Found " + str(counter) + " mods")

    print(modids)
    
    success = True

    return success;

userDefinedPath = ""

choice1 = "" 
useDefaultPath = True

def yesno():
    while True:
        print("[y/n]")
        choice1 = input()
        choice1 = choice1.lower()
        if choice1 == 'y':
            return True
            break
        elif choice1 == 'n':
            return False
            break
        


print("Use default path for settings file? (" + str(filepath1) + ")")
useDefaultPath = yesno()

if not useDefaultPath:
    # print("Please enter user defined read path (not including file name)")
    # userDefinedPath = input()
    # userDefinedPath = Path(userDefinedPath)
    print("Opening file dialog...")
    root = tkinter.Tk()
    root.withdraw()
    userDefinedPath = Path(filedialog.askdirectory(title = "Select Hearts of Iron IV Documents folder"))
    filepath1 = userDefinedPath / filename

"""
if useDefaultPath:
    filepath2 = filepath1
else:
    filepath2 = userDefinedPath
"""

ReadFile(filepath1)