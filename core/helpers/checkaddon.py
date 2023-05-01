import os
from pyroub import LOGGER, eor

config_exists = os.path.exists("config.py")

#Addons
if config_exists:
    try:
        from config import ENABLE_ADDONS
    except:
        LOGGER.info("Addons Option Not Found, Not installing Addons")
        ENABLE_ADDONS = "DISABLE"
else:
    try:
        from sample_config import ENABLE_ADDONS
    except:
        LOGGER.info("Addons Option Not Found, Not installing Addons")
        ENABLE_ADDONS = "DISABLE"

def CheckAddons():
    if ENABLE_ADDONS.lower() == "enable":
        return True
    elif ENABLE_ADDONS.lower() == "disable":
        return False
    else:
        LOGGER.info("Undefined Addons Argument! Not Installing Addons")
        return False

#ExtraInstaller
if config_exists:
    try:
        from config import SELF_INSTALLER
    except:
        LOGGER.info("SelfInstaller Option Not Found, Not Allowing Installer")
        SELF_INSTALLER = "DISABLE"
else:
    try:
        from sample_config import SELF_INSTALLER
    except:
        LOGGER.info("SelfInstaller Option Not Found, Not Allowing Installer")
        SELF_INSTALLER = "DISABLE"
        
def CheckSelfInstaller():
    if SELF_INSTALLER.lower() == "enable":
        return True
    elif SELF_INSTALLER.lower() == "disable":
        return False
    else:
        LOGGER.info("SelfInstaller Option Undefined, Not Allowing Installer")
        return False