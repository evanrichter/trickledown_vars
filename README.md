# Trickle-Down Variables (v0.1 alpha)
Author: **toolCHAINZ**

Autorename variables that are copies of other variables._
## Description:
A lot of MLIL variables don't do anything, and just shuttle data from location to location.

By looking at MLIL var definitions and uses, it is possible to identify these trivial cases and automatically rename the variables involved.
## Minimum Version

This plugin requires the following minimum version of Binary Ninja:

 * dev - 1.1.1016-dev


## Required Dependencies

The following dependencies are required for this plugin:



## License
This plugin is released under a [MIT](LICENSE) license.

## Usage
After opening a new binary view, select `Autorename Variables` from the right-click menu and start renaming MLIL variables

## Known Issues
This plugin works by renaming variables whose contents are a copy of other variables. You'll want to only rename variables which don't have this kind of dependency on another varaible because otherwise the script will blow away your changes. Not sure how to avoid that...
