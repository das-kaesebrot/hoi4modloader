from pathlib import Path
import os
import time
# import re
import string
import platform
import tkinter
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
# set this to False to turn off automatic backups when making changes to settings.txt file
doBackup = True
# set this to True to use a config file to set the above 3 options
useconfigFile = True

##########################################################################################

currentVersion = "1.0.15"

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
    print("Custom export path: DEACTIVATED")

if not doBackup:
    print("\nAutomatic backup: DEACTIVATED")

filename = "settings.txt"
filepath1 = Path(defaultpath) / filename

# ModsDetected = False

def ReadFile1(filepath):
    print("")
    
    exists = os.path.isfile(filepath)
    if not exists:
        input("ERROR: File not found\nAborting script\nPress any key to exit...")
        quit()

    # readlines = False
    # stopReadingNext = False
    
    counter = 0
    f = open(filepath, 'r')
    copyModId = []

    print("Reading settings.txt")

    for line in f:
        
        """
        if "last_mods" in line:
            readlines = True
        elif "}" in line and readlines:
            stopReadingNext = True
        if readlines:
            copyModId.append(line)
        if stopReadingNext:
            readlines = False
        
        # Keeping this for later for optional Steam API support        
        
        if ".mod" in line and readlines:
            temp = line
            temp = re.sub("\D", "", temp)
            modids.append(int(temp))
            counter += 1
        """

        if ".mod" in line:
            copyModId.append(line)
            counter += 1
        
    if counter == 0:
        print("No mods detected in settings.txt")
    else:
        print("Found " + str(counter) + " active mod(s) in settings.txt")
        # ModsDetected = True

    f.close()

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
            break
        elif choice1 == 'n':
            return False
            break
        

if not overrideDefaultPath:
    print("Use default path for settings file? (" + str(filepath1) + ")")
    useDefaultPath = yesno()

if not useDefaultPath:
    print("Opening file dialog...")
    root = tkinter.Tk()
    root.withdraw()
    defaultpath = Path(filedialog.askdirectory(title = "Select Hearts of Iron IV Documents folder"))
    filepath1 = defaultpath / filename

HOI4ModList = ReadFile1(filepath1)

def exportModList(List1):
    filenameExport = "modlist_" + time.strftime("%Y%m%d-%H%M%S") + ".txt"
    # custom Path override
    outpath = defaultpath
    if setCustomOutputPath:
        outpath = Path(userDefinedOutputPath)
    
    f = open(Path(outpath) / filenameExport, "x")
    for item in HOI4ModList:
        f.write(item)
    print("Successfully wrote mod list to " + str(Path(outpath) / filenameExport))
    f.close()
    return

def importModList():
    print("Please select file to import mod list from")
    filepathImport = Path(getFilePath())

    counter = 0
    importedModList = []
    f = open(filepathImport, 'r')

    for line in f:
        if ".mod" in line:
            importedModList.append(line)
            counter += 1
    
    print("Found " + str(counter) + " mod(s) in file")

    if doBackup:
        filenameBackup = time.strftime("settings_backup_" + "%Y%m%d-%H%M%S") + ".txt"

        f2 = open(filepath1, 'r')
        f3 = open(Path(defaultpath) / filenameBackup, 'x')
        for line in f2:
            f3.write(line)
        f2.close()
        f3.close()
        print("Wrote backup of settings.txt to " + str(Path(defaultpath) / filenameBackup))
    else:
        print("Skipping backup of settings.txt")
    
    print("Replacing mod(s)...")

    tempFilename1 = "settings.txt.part1.TEMP"
    tempFilename2 = "settings.txt.part2.TEMP"

    # skipLines = False
    part1Done = False
    part2Write = False
    announcePart1Done = False

    f_settings_old = open(filepath1, 'r')
    f_settings_temp1 = open(Path(defaultpath) / tempFilename1, 'x')
    f_settings_temp2 = open(Path(defaultpath) / tempFilename2, 'x')
    for line in f_settings_old:
        # if not skipLines and not part1Done:
            # f_settings_temp1.write(line)
        # if "last_mods" in line:
            # skipLines = True
        # elif "}" in line and skipLines:
            # part1Done = True
        if not part1Done:
                f_settings_temp1.write(line)
        if "hints=" in line:
            announcePart1Done = True
            # if not ModsDetected:
                # skipLines = True
        if "counter_color_mode=" in line:
            part2Write = True
        if part1Done and part2Write:
            f_settings_temp2.write(line)
        if announcePart1Done:
            part1Done = True

    f_settings_old.close()
    f_settings_temp1.close()
    f_settings_temp2.close()

    f_settings_temp1 = open(Path(defaultpath) / tempFilename1, 'r')
    f_settings_temp2 = open(Path(defaultpath) / tempFilename2, 'r')
    
    os.remove(filepath1)

    f_settings_new = open(filepath1, "x")
    for line in f_settings_temp1:
        f_settings_new.write(line)
    
    f_settings_temp1.close()

    # somehow this doesn't work?
    """
    for line in f:
        if ".mod" in line:
            f_settings_new.write(line)
    """
    
    # if not ModsDetected:
    #     f_settings_new.write("last_mods={\n")
    
    f_settings_new.write("last_mods={\n")

    for line in importedModList:
        f_settings_new.write(line)
    
    f_settings_new.write("}\n")
    
    # if not ModsDetected:
    #     f_settings_new.write("}\n")

    f.close()

    for line in f_settings_temp2:
        f_settings_new.write(line)

    f_settings_temp2.close()
    os.remove(Path(defaultpath) / tempFilename1)
    os.remove(Path(defaultpath) / tempFilename2)
    
    f_settings_new.close()

    print("Done!")

def clearModList():

    if doBackup:
        filenameBackup = time.strftime("settings_backup_" + "%Y%m%d-%H%M%S") + ".txt"

        f2 = open(filepath1, 'r')
        f3 = open(Path(defaultpath) / filenameBackup, 'x')
        for line in f2:
            f3.write(line)
        f2.close()
        f3.close()
        print("Wrote backup of settings.txt to " + str(Path(defaultpath) / filenameBackup))
    else:
        print("Skipping backup of settings.txt")
    
    print("Clearing mod(s)...")

    tempFilename1 = "settings.txt.part1.TEMP"
    tempFilename2 = "settings.txt.part2.TEMP"

    # skipLines = False
    part1Done = False
    part2Write = False
    announcePart1Done = False

    f_settings_old = open(filepath1, 'r')
    f_settings_temp1 = open(Path(defaultpath) / tempFilename1, 'x')
    f_settings_temp2 = open(Path(defaultpath) / tempFilename2, 'x')
    for line in f_settings_old:
        if not part1Done:
                f_settings_temp1.write(line)
        if "hints=" in line:
            announcePart1Done = True
        if "counter_color_mode=" in line:
            part2Write = True
        if part1Done and part2Write:
            f_settings_temp2.write(line)
        if announcePart1Done:
            part1Done = True

    f_settings_old.close()
    f_settings_temp1.close()
    f_settings_temp2.close()

    f_settings_temp1 = open(Path(defaultpath) / tempFilename1, 'r')
    f_settings_temp2 = open(Path(defaultpath) / tempFilename2, 'r')
    
    os.remove(filepath1)

    f_settings_new = open(filepath1, "x")
    for line in f_settings_temp1:
        f_settings_new.write(line)
    
    f_settings_temp1.close()

    for line in f_settings_temp2:
        f_settings_new.write(line)

    f_settings_temp2.close()
    os.remove(Path(defaultpath) / tempFilename1)
    os.remove(Path(defaultpath) / tempFilename2)
    
    f_settings_new.close()

    print("Done!")

def getFilePath():
    print("Opening file dialog...")
    root = tkinter.Tk()
    root.withdraw()
    userDefinedPath = Path(filedialog.askopenfilename(title = "Select Text File"), filetypes = (("Text files","*.txt"),("all files","*.*")))
    return str(userDefinedPath)

print("")
while True:
    print("Please choose an option:\n[1] Import mod list to HOI4 from file ($CustomFile.txt -> settings.txt)\n[2] Export mod list from HOI4 to file (settings.txt -> $CustomFile.txt)\n[3] Clear mods from settings.txt\n[q] Abort script")
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

input("\nPress any key to exit script... ")