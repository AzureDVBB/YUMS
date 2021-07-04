#
print(f'Invoking __init__.py for {__name__}')

# in order to import as package, use this form on each imported module
# 'from . import' implies that modules are imported from this exact package
# so please use this form as the implicit "import tests" doesn't work on deeply
# nested packages from my experience
from . import funcs
from . import clas

# the user is responsible for updating the PACKAGES list alongside the 'importing' of them
PACKAGES = [funcs,clas]

def compile_implemented_list_for_packages(PACKS):
    # get all implemented function keys from all packages
    implemented_keys = []
    for P in PACKS:
        for key in P.IMPLEMENTED.keys():
            implemented_keys.append(key.lower()) # ensure lower/upper case doesn't matter
    # check for duplicates by comparing list length between a the list and it's set
    duplicates = not (len(implemented_keys) == len(set(implemented_keys)))

    # throw an error if there is a duplicate
    result = {}
    if duplicates:
        raise ImportError("Duplicate keys found in packages' IMPLEMENTED")

    else:
        for P in PACKS:
            result.update(P.IMPLEMENTED)

    return result

# the complete list of implemented functions/classes for the lookup module
IMPLEMENTED = compile_implemented_list_for_packages(PACKAGES)

del compile_implemented_list_for_packages # remove function reference from scope