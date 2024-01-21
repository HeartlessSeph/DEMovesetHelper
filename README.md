# LaD Gaiden Moveset Helper Readme

## Overview
This program assists in creating movesets for LaD Gaiden. It's named DE moveset helper because it may work with other DE games, but this was specifically designed for Gaiden. Bugs encountered in those games will not be addressed. This project is designed for editing Gaiden movesets, and feature requests will not be considered. The primary goal is to streamline moveset editing without manual file linking and reduce busy-work.

## Workspace Creation
1. Create a folder for your project.
2. Place extracted db jsons in the folder (filename.json, not filename.bin.json).
3. Check Supported Bins.txt for supported files.
4. Drag and drop the folder onto extract.bat.
5. The program creates folders (MBV, Motion, Patches, Workspace) containing base files for editing and exporting.

## Project Building
1. To compile changes, drag and drop the folder onto build.bat.
2. A build folder will be created with updated changes.

## Motion Folder
- Contains edited or new gmt and bep files.
- bep and gmt files do not need to be in any specific folders. Folders and subfolders can be used.
- I suggest structuring it like motion.par. If my project contains multiple movesets, I like to break the files up into multiple folders (eg: Moveset1/bep, Moveset1/gmt, Moveset2/bep, Moveset2/gmt).
- Files in this folder are auto-patched into motion_gmt and motion_bep during program building.

## MBV Folder
- Contains MBVs and json edits.
- Requires motion_gmt.json to be in the project folder.
- After the initial workspace creation, place any MBVs you want to edit into the MBV Folder. Then drag the project folder onto extract.bat to extract MBVs.
- Edit MBV.json fields; it will be built when dragging onto build.bat.
- MBVs can be renamed (json must also be renamed) and any new MBVs will be auto-added into behavior_set.

## Patches Folder
- Holds patches for Workspace files.
- Patch filenames should begin with the name of the file you want to patch.
- Files in patch folder do not need to have any particular structure, you can put the .json patches into folders or subfolders for organization purposes.
- Patch structure should make the original file being patched. If adding a new entry to that file, you need to add every column to the new entry but this isn't necessary if only editing an entry (see example patch).

## Fighter Command
- Supports Fighter Command patches.
- Use Fighter Commander to extract the cfc.
- Required files: motion_gmt and talk_param.
- Place "File Information.json" and Fighter Command folder in the base project folder.
- Patch cfc by placing the new moveset into the patches folder (e.g., "cfc (p_kiryu_ouryu2).json").
- Cfc patching requires the -cfc argument during building.

## reARMP Support
- Auto-rebuild the output json files using reARMP with the -rearmp argument.
- Use -rearmp "Path/To/reARMP/reARMP.exe" during building.
