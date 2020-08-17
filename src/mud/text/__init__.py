"""
Useful manipulation tools for working with strings, now with re-loading support!
"""

import sys as __sys
import importlib as __importlib

# names of the python modules/packages (folder/file name with no extension)
__all__ = ['split', 'help_format']

### Runtime Module Reloading support #############################
##################################################################
__importlib.invalidate_caches()

for __mod in __all__:
    if __mod in dir():
        __importlib.reload(__sys.modules[f"{__name__}.{__mod}"])

del __mod
##################################################################

from . import * # load all modules with filenames defined by '__all__'