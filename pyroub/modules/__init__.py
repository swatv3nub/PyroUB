import glob
import importlib
from os.path import basename, dirname, isfile, join

from core.helpers.checkaddon import CheckAddons

"""
if CheckAddons() is True:
    path = "addons." + plugin_name
    importlib.import_module(path)
    
else:
    pass
"""  

modules = glob.glob(join(dirname(__file__), "*.py"))
    __all__ = [
    basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
    ]
    