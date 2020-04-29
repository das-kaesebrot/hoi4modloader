from pathlib import Path
import os
import time
import string
import platform
import tkinter
import json
from tkinter import filedialog
import configparser

### PROGRAM VARIABLES FOR CUSTOMIZATION ###################################################

# enable this to override checking for path
overrideDefaultPath = False
# Paste your custom path to the HOI4 doc folder here if above option is enabled
userDefinedPath1 = ""
# enable this to override the mod list output folder to a custom path (Next option)
setCustomOutputPath = False
# Paste your custom path to the output folder the mod list files should be exported to here
userDefinedOutputPath = ""
# set this to False to turn off automatic backups when making changes to dlc_load.json file
doBackup = True
# set this to True to use a config file to set the above 3 options
useconfigFile = True

##########################################################################################

currentVersion = "2.0.1"

print("\n\thoi4modloader, version " + currentVersion)
print("\tScript written by")
print("\tKaesebrot - @das_kaesebrot\n")
print("### ATTENTION ###")
print("Do not run this script while Hearts of Iron IV or the Hearts of Iron IV launcher are running!\n")

config = configparser.ConfigParser()

if useconfigFile:
    # Generates a config file next to the script
    configname = "config.ini"
    if not os.path.isfile(Path(os.curdir) / configname):
        print("Generating config file...\n")
        config['Switches'] = {'overrideDefaultPath': 'no',
                            'setCustomOutputPath': 'no',
                            'doSettingsBackup': 'yes'}
        config['Paths'] = {'userDefinedInput': '',
                            'userDefinedOutput': ''}
        with open(configname, 'w') as configfile:
            config.write(configfile)
    
    # Reads config file values
    else:
        print("Reading config file...\n")
        config.read(configname)
        overrideDefaultPath = config['Switches'].getboolean('overrideDefaultPath')
        setCustomOutputPath = config['Switches'].getboolean('setCustomOutputPath')
        doBackup = config['Switches'].getboolean('doSettingsBackup')
        userDefinedPath1 = config['Paths'].get('userDefinedInput')
        userDefinedOutputPath = config['Paths'].get('userDefinedOutput')

currentOS = platform.system()

def setdefaultPath(currentOS):
    path = ""
    if currentOS == "Linux":
        path = os.path.join(os.path.expanduser('~'),".local","share","Paradox Interactive","Hearts of Iron IV")
    elif currentOS == "Darwin":
        path = os.path.join(os.path.expanduser('~'),"Documents","Paradox Interactive","Hearts of Iron IV")
        currentOS = "macOS"
    elif currentOS == "Windows":
        path = os.path.join(os.path.expandvars("%userprofile%"),"Documents","Paradox Interactive","Hearts of Iron IV")
    else:
        path = ""
        print("Unable to detect OS, please point to HOI4 Documents folder manually")
        return
    print("Detected OS: " + currentOS)
    print("Default path was automatically set to: " + path + "\n")
    
    path2 = Path(path)
    return path2

if overrideDefaultPath:
    defaultpath = userDefinedPath1
    print("Default path override: ACTIVATED")
    print("Setting path to " + defaultpath)
else:
    print("Default path override: DEACTIVATED")
    defaultpath = setdefaultPath(currentOS)

if setCustomOutputPath:
    print("Custom export path: ACTIVATED")
    print("Setting mod list export path to " + userDefinedOutputPath)
else:
    print("Custom export path: DEACTIVATED\n")

if not doBackup:
    print("\nAutomatic backup: DEACTIVATED")

filename = "dlc_load.json"
path1 = Path(defaultpath)

def getJSONDict(filepath1):
    print("")
    exists = os.path.isfile(filepath1)
    if not exists:
        input("ERROR: File not found\nAborting script\nPress any key to exit...")
        quit()
    
    f = open(filepath1, 'r')
    readDict = json.load(f)
    f.close()
    return readDict

def ReadFile1(filepath):
    dlc_load_dict = getJSONDict(filepath / filename)

    copyModId = dlc_load_dict.get("enabled_mods")

    print("Reading " + filename)
        
    if not copyModId:
        print("No mods detected in  " + filename)
    else:
        print("Found " + str(len(copyModId)) + " active mod(s) in " + filename)
        
    return copyModId

userDefinedPath = ""

choice1 = "" 
useDefaultPath = True

def yesno():
    while True:
        # print("[y/n]")
        choice1 = input("[y/n] > ")
        choice1 = choice1.lower()
        if choice1 == 'y':
            return True
            # break
        elif choice1 == 'n':
            return False
            # break
        

if not overrideDefaultPath:
    print("Use default path for " + filename + " file? (" + str(path1 / filename) + ")")
    useDefaultPath = yesno()

if not useDefaultPath:
    print("Opening file dialog...")
    root = tkinter.Tk()
    root.withdraw()
    defaultpath = Path(filedialog.askdirectory(title = "Select Hearts of Iron IV Documents folder"))
    path1 = defaultpath

HOI4ModList = ReadFile1(path1)

def exportModList(List1):
    filenameExport = "modlist_" + time.strftime("%Y%m%d-%H%M%S") + ".json"
    # custom Path override
    outpath = defaultpath
    if setCustomOutputPath:
        outpath = Path(userDefinedOutputPath)

    dictModList = {'enabled_mods': HOI4ModList}

    with open(Path(outpath) / filenameExport, 'w') as fp:
        json.dump(dictModList, fp)

    print("Successfully wrote mod list to " + str(Path(outpath) / filenameExport))
    return

def importModList():
    print("Please select file to import mod list from")
    
    filepathImport = Path(getFilePath())
    
    f = open(filepathImport, 'r')
    dlc_load_dict = getJSONDict(filepathImport)
    f.close()
    copyModId = dlc_load_dict.get("enabled_mods")
    
    print("Found " + str(len(copyModId)) + " active mod(s) in file")

    if doBackup:
        filenameBackup = time.strftime("dlc_load_backup_" + "%Y%m%d-%H%M%S") + ".json"

        f2 = open(path1 / filename, 'r')
        f3 = open(Path(defaultpath) / filenameBackup, 'x')
        for line in f2:
            f3.write(line)
        f2.close()
        f3.close()
        print("Wrote backup of " + filename + " to " + str(Path(defaultpath) / filenameBackup))
    else:
        print("Skipping backup of " + filename)
    
    print("Replacing mod(s)...")

    f_settings_old = open(path1 / filename, 'r')
    dictDLCLoadJSON = json.load(f_settings_old)
    f_settings_old.close()
    os.remove(path1 / filename)

    dictDLCLoadJSON["enabled_mods"] = copyModId

    with open(path1 / filename, 'x') as fp:
        json.dump(dictDLCLoadJSON, fp)

    print("Done!")

def clearModList():

    if doBackup:
        filenameBackup = time.strftime("dlc_load_backup_" + "%Y%m%d-%H%M%S") + ".json"

        f2 = open(path1 / filename, 'r')
        f3 = open(Path(defaultpath) / filenameBackup, 'x')
        for line in f2:
            f3.write(line)
        f2.close()
        f3.close()
        print("Wrote backup of " + filename + " to " + str(Path(defaultpath) / filenameBackup))
    else:
        print("Skipping backup of " + filename)
    
    print("Clearing mod(s)...")

    f_settings_old = open(path1 / filename, 'r')
    dictDLCLoadJSON = json.load(f_settings_old)
    f_settings_old.close()
    os.remove(path1 / filename)

    dictDLCLoadJSON.pop("enabled_mods")

    with open(path1 / filename, 'x') as fp:
        json.dump(dictDLCLoadJSON, fp)

    print("Done!")

def getFilePath():
    print("Opening file dialog...")
    root = tkinter.Tk()
    root.withdraw()
    userDefinedPath = Path(filedialog.askopenfilename(title = "Select " + filename + " File"), filetypes = (("JSON files","*.json"),("all files","*.*")))
    return str(userDefinedPath)

print("")
while True:
    print("Please choose an option:\n[1] Import mod list to HOI4 from file ($CustomFile.json -> " + filename + ")\n[2] Export mod list from HOI4 to file (" + filename + " -> $CustomFile.json)\n[3] Clear mods from " + filename + "\n[q] Abort")
    choice2 = input("> ").lower()
    if choice2 == "1":
        importModList()
        break
    elif choice2 == "2":
        exportModList(HOI4ModList)
        break
    elif choice2 == "3":
        clearModList()
        break
    elif choice2 == "q":
        break
    else:
        print("\n#########\nERROR: No valid input provided")

input("\nPress any key to exit... ")