#
print(f'Invoking __init__.py for {__name__}')

# in order to import as package, use this form on each imported module
# 'from . import' implies that modules are imported from this exact package
# so please use this form as the implicit "import tests" doesn't work on deeply
# nested packages from my experience
from . import tests

# List of implemented functions/classes in the package
# WARN: ENSURE ALL KEYS ARE LOWER CASE AT ALL TIMES ELSE PROBLEMS FOLLOW
IMPLEMENTED = {'test1': tests.test1, 'test2': tests.test2}