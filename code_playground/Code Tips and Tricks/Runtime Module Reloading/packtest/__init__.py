"""
Testing package level reload.
"""
import importlib


# check if modules allready loaded
if not ('testing' in dir()):# load package if it is not yet loaded
    from . import testing # must use relative import if same named module

else: # reload package if allready loaded in
    importlib.reload(testing)

# init script running
variable = "test 3"
print(variable)
