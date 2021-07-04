#### The fantastically awesome modular, reloadable command interpreter!
##### now with fewer lines to edit and gotchas!

This is an example for both using README.md in a folder in github as well as  an example design
of a modular, as easily extendable as possible, command interpreter.

###### Extendability

The entire package resides in `commands`, the `commands/__init__.py` houses the class `Interpreter`
which needs to be updated with logic to handle commands. It also houses the logic for loading and
and re-loading logic of the subpackages, and in order to add another subpackage the `__all__`
list must be updated to add it to the loading, and also the `Interpreter` class updated
with logic to handle it.

Subpackages under `commands/admin_level` and `commands/user_level` are the collection of
command handlers, seperated into different levels of access based on player types.
Their `__init__.py` scripts once again are for aggregating, loading and re-loading all of the
modules inside them, the `__all__` list inside there needs to be updated with all the modules
that has the command handlers.

Individual modules `example1.py` for instance must have the handler function defined,
taking three arguments: `player`, `database`, `message` as they will be used to handle them.
The modules must also contain a dictionary at the bottom of the file called `COMMANDS`
that will hold the command that the player will need to send as its key, and the reference
to the handler function as its value.

`commands/user_level/packexample` is an example for hiding a more complex command handler, or
collection of commands. `example3.py` inside shows how to implement the loading and re-loading
of the `helper.py` module that is only used in there and not defining any commands.
On a small side effect, the first run the helper module will be loaded in twice, so any
side effects that might happen will need to be taken into account. However re-loading works fine.
Notice how the `__init__.py`  in here is near identical to `commands/user_level/__init__.py`

To see this all this in action, try running `command_reload_testing.py`