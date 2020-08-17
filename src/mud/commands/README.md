# Command Interpreter

The kickin' modular and runtime re-loadable command interpreter!
AKA: the backbone of any MUD

---

### Quick start guide to making a new command

1. copy and rename template.py to something sensible.

1. rename the function definition to something sensible.

1. replace `pass` with the logic handling (see modules in `user_level` for examples).

1. update the `COMMANDS` dictionary with the string name the command will look for (no spaces allowed) as the key, and the function reference (the name of the function, not string) as its value.

1. update the `__all__` list with the name of the new file (without the .py extension) in the  `__init__.py` file in the same folder as the new module.

---

### Quick start guide to making a new package holding many commands

1. copy and rename the `template` folder.

2. go through the *quick start guide to making a new command* and make commands in it.

3. update the `__all__` list with the name of the new folder in the `__init__.py` file in the same folder where your new package is located.

---

# A more in-depth look

### The interpreter

Inside the `__init__.py` file is the `Interpreter` class which does two things:

* Initialize a class instance with:
	* A `Database` object instantiated with the class
	* A reference to the `Manager` object 
* Give a convenience method `process` that takes in `player_name` and `message` arguments.

##### The `process` method

This forms the main switching logic for actually interpreting the commands.

It takes only two strings as arguments, `player_name` and `message`. The former is the name of the player who sent the message, the latter is the message that has been sent, as-is.

It first seperates the first word of the `message` argument and checks if its a key in the `COMMANDS` dictionary, this is a check to see if the command sent is an implemented command. 

It then proceeds to make a check if the command is followed by the literal string `#help` and will send the associated documentation of the command if it is.

Otherwise it will call the function associated with the command, passing in the following argumens:

* `Database` object (the connection to the database and associated helper methods)
* `Manager` object (for interacting with connected players and the MUD itself)
* `player_name` (name of the player who sent the command)
*  `message` (the remaining message without the first word)

##### ... the `COMMANDS` dictionary?

It's the main way of implementing the commands themselves. It holds each understood command text as a key to finding the associated function that handles it's execution.

Every module that makes a new command __must__ have a `COMMANDS` dictionary. If creating a new package, those packages have to take those dictionaries and combine them into a single `COMMANDS` dictionary.

See `template.py` and the `template` package (folder), or a live example under the `user_level` package.


### The modules implementing the commands

Also known as: The business logic.

These are simple functions that take in 4 arguments as discussed above, `Database`, `Manager`, `player_name` and `message`.

The `Database` and `Manager` objects are used to interact with the MUD itself, move players, interact with the database, send/recieve messages etc. For more information on them, see their respective `README.md` files at `src/mud/manager` and `src/mud/database`.

The `player_name` and `message` strings are used to identify the player calling the function and the message is the actual argument for the function.

Lastly, they have to have a `COMMANDS` dictionary (preferrably at the bottom of the file) that binds the actual command, that is the first word players have to send in their message, to the function that will handle it.

Writing the commands themselves is left to the enterprising creator that will use this framework. They can make it as complicated or as simple as they like, as long as it always takes those 4 arguments, and implement a `COMMANDS` dictionary.

For concrete examples please see the allready written commands under the `user_level` folder.