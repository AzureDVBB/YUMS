from . import login

# NOTE: list of packages, keep up to date along with the imports
PACKAGES = [login,]

def compile_implemented_list_for_packages():
    # get all implemented function keys from all packages
    implemented_keys = []
    for P in PACKAGES:
        for key in P.IMPLEMENTED.keys():
            implemented_keys.append(key.lower()) # ensure lower/upper case doesn't matter
    # check for duplicates by comparing list length between a the list and it's set
    duplicates = not (len(implemented_keys) == len(set(implemented_keys)))

    # throw an error if there is a duplicate
    result = {}
    if duplicates:
        raise ImportError("Duplicate keys found in packages' IMPLEMENTED")

    else:
        for P in PACKAGES:
            result.update(P.IMPLEMENTED)

    return result

IMPLEMENTED = compile_implemented_list_for_packages()

del compile_implemented_list_for_packages