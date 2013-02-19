#!/usr/bin/env python

import sys
import os

from SteamShortcutManager import SteamShortcutManager

import SteamInstallationLocationManager
import SteamUserManager
import IceSettings
import IceConsole
from IceROM import ROM
from IceROMManager import IceROMManager
from IceGridImageManager import IceGridImageManager
from IceLogging import log

def main():
    log("=========================Starting Ice")
    # Find all of the ROMs that are currently in the designated folders
    roms = IceConsole.find_all_roms()
    # Find the Steam Account that the user would like to add ROMs for
    user_ids = SteamUserManager.user_ids_on_this_machine()
    for user_id in user_ids:
        log("---------------Running for user %s" % str(user_id),2)
        # Load their shortcuts into a SteamShortcutManager object
        shortcuts_path = SteamUserManager.shortcuts_file_for_user_id(user_id)
        shortcuts_manager = SteamShortcutManager(shortcuts_path)
        rom_manager = IceROMManager(shortcuts_manager)
        # Add the new ROMs in each folder to our Shortcut Manager
        rom_manager.sync_roms(roms)
        # For testing purposes, uncomment this code, which will save the new
        # shortcuts.vdf file in updated_shortcuts.vdf instead of overwriting
        # the old file
        # 
        # shortcuts_dir = os.path.dirname(shortcuts_path)
        # my_path = os.path.join(shortcuts_dir,"updated_shortcuts.vdf")
        # shortcuts_manager.save(my_path)
        # 
        # Generate a new shortcuts.vdf file with all of the new additions
        shortcuts_manager.save()
    log("---------------Downloading grid images for games",2)
    grid_manager = IceGridImageManager()
    for user_id in user_ids:
        grid_manager.update_user_images(user_id,roms)
        
if __name__ == "__main__":
    main()