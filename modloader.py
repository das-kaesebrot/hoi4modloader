from pathlib import Path
import os
import time
import re
import string
import platform
import tkinter
from tkinter import filedialog

currentOS = platform.system()

# enable this to override checking for path
overrideDefaultPath = True
# Paste your custom path here if above option is enabled
userDefinedPath1 = "D:\Kaesebrot\Documents\Paradox Interactive\Hearts of Iron IV"

print("### ATTENTION ###")
print("Do not run this script while Hearts of Iron IV or the Hearts of Iron IV launcher are running!\n")

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
    defaultpath = userDefinedPath1
    print("Default path override: ACTIVATED")
    print("Setting path to " + defaultpath)
else:
    print("Default path override: DEACTIVATED")
    defaultpath = setdefaultPath(currentOS)

filename = "settings.txt"
filepath1 = Path(defaultpath) / filename

"""
def ReadFileStatus():
    status = ReadFile(filepath1)
    if status:
        labeltext = "File read successfully"
    else:
        labeltext = "Error reading file"

    return;
"""

def ReadFile1(filepath):
    print("")
    
    exists = os.path.isfile(filepath)
    if not exists:
        print("ERROR: File not found")
        return

    readlines = False
    stopReadingNext = False

    counter = 0

    f = open(filepath, 'r')

    print("Reading settings.txt")

    # modids = []
    copyModId = []

    for line in f:
        
        if "last_mods" in line:
            readlines = True
        elif "}" in line and readlines:
            stopReadingNext = True
        if readlines:
            copyModId.append(line)
        if stopReadingNext:
            readlines = False
        """
        if ".mod" in line and readlines:
            temp = line
            temp = re.sub("\D", "", temp)
            modids.append(int(temp))
            counter += 1
        """
        if ".mod" in line and readlines:
            counter += 1
        
    print("Found " + str(counter) + " active mods in settings.txt")

    # print(modids)

    f.close()

    return copyModId

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
        

if not overrideDefaultPath:
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

HOI4ModList = ReadFile1(filepath1)

def exportModList(List1):
    filenameExport = time.strftime("%Y%m%d-%H%M%S") + ".txt"
    # print("\nExported file will be called " + str(filenameExport))
    # print("Exported file will be written to " + str(defaultpath))
    f = open(Path(defaultpath) / filenameExport, "x")
    for item in HOI4ModList:
        f.write(item)
    print("Successfully wrote mod list to " + str(Path(defaultpath) / filenameExport))
    f.close()
    return

def importModList():
    print("Please select file to import mod list from")
    filepathImport = Path(getFilePath())

    counter = 0

    f = open(filepathImport, 'r')

    readlines = False
    stopReadingNext = False

    ImportedModList = []

    for line in f:
        if "last_mods" in line:
            readlines = True
        elif "}" in line and readlines:
            stopReadingNext = True
        if readlines:
            ImportedModList.append(line)
        if stopReadingNext:
            readlines = False
        """
        if ".mod" in line and readlines:
            temp = line
            temp = re.sub("\D", "", temp)
            modids.append(int(temp))
            counter += 1
        """
        if ".mod" in line and readlines:
            counter += 1
    
    print("Found " + str(counter) + " mods in file")

    filenameBackup = time.strftime("settings_backup_" + "%Y%m%d-%H%M%S") + ".txt"

    f2 = open(filepath1, 'r')
    f3 = open(Path(defaultpath) / filenameBackup, 'x')
    for line in f2:
        f3.write(line)
    f2.close()
    f3.close()
    print("Wrote backup of settings.txt to " + str(Path(defaultpath) / filenameBackup))


def getFilePath():
    print("Opening file dialog...")
    root = tkinter.Tk()
    root.withdraw()
    userDefinedPath = Path(filedialog.askopenfilename(title = "Select Text File"), filetypes = (("Text files","*.txt"),("all files","*.*")))
    return str(userDefinedPath)

print("")
while True:
    print("Please choose an option:\n[1] Import mod list to HOI4 from file ($CustomFile.txt -> settings.txt)\n[2] Export mod list from HOI4 to file (settings.txt -> $CustomFile.txt)")
    choice2 = input()
    if choice2 == "1":
        importModList()
        break
    elif choice2 == "2":
        exportModList(HOI4ModList)
        break
    else:
        print("\n#########\nERROR: No valid input provided")