## About this program
This is a small program to import/export mod lists from your Hearts of Iron IV installation, which is achieved by modifying the launcher's ``dlc_load.json`` file.
In order for this to work, you need to have all mods you're importing installed.

You can find a standalone Windows executable and a Linux binary (generated using PyInstaller) under [Releases](https://github.com/das-kaesebrot/hoi4modloader/releases).

You can use the provided ``config.ini`` to override the default path in which the script looks for the ``dlc_load.json`` file.
The config file will be automatically generated next to the executable/binary if it doesn't exist yet.

## Prerequisites (if you're not using the binaries)
``Python 3``

## Other
This might possibly also work with other Paradox games that use the Paradox Launcher, haven't tested it yet though.