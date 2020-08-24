### Datatypes

AKA: dataclasses for the forgetful programmer to know what the blazes is stored in the database.

### Basic usage

While it can be used standalone, it is encouraged to use existing database objects (see one directory up) as they hold a reference to this module allready. And propably are kept up to date during runtime re-loads.

Classes described here are nothing more then dataclasses with convenience methods and properties. the following are some common convenience methods/properties:

**asdict** gets the dictionary representation of the dataclass, basically calling `dataclass.asdict(obj)`.

**from_dict** constructs the dataclass from a dictionary. Raising `KeyError` when the dictionary does not have the required keys.

Don't like the functionality/datatypes? Change them!

### Extending with more datatypes

1. Create a new python file
1. Define the new datatypes as classes/dataclasses
1. Add the import statement to the `__init__.py` using relative import. (`from .mymodule import MyDataclass`)
1. (bonus) add `asdict` property and `from_dict` method akin to other datatypes

Done! It is now usable after loading/re-loading the datatypes module.