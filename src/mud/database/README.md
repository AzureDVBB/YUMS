# Database
A thin wrapper for all things low level, and extensible amount of methods to abstract away common database operations.

---

#### The underlying backend

**Mongo DB** is used as the underlying database engine. You can learn more about how it works and it's advanced features that it has at it's website: <https://docs.mongodb.com/manual/> (yes I am linking the documentation and not the corporate shill main website.)

***in brief:*** it stores **documents** (esentially python dictionaries) grouped in named **collections** that are all held in named **databases**. Each **document** (dictionary) can have multiple **fields** (key/value pairs) which can hold data, arrays or documents.

**Motor** is used as the asynchronous python package to connect to the MongoDB database. For more information on how it works visit it's website: <https://motor.readthedocs.io/en/stable/> , we use the **asyncio** backend of it (because python3.6+) but it can also work with thornado too!

***in brief:*** it allows us to connect to the database, and access collections like a dictionary. Example: `database['my_database']['my_collection']` will return a reference to the `my_collection` collection in the `my_database` database, and lets us use coroutines to manipulate documents inside of it.

---

#### The Database class

Located in `__init__.py` it holds the initialization of a database connection, the methods to abstract away common and/or complicated database operations. 

**class variables** hold the names of the databases, and collections inside those databases that store for example, user data and world data. Need another database/collection to sore something? This is the first place to go to add it. It also has a `datatypes` variable, holding a reference to that package. More on it later.

**initializing** the class will create a database connection as well ass initialize, and store a reference to all of the helper classes that hold the above mentioned methods abstracting away common or complicated operations.

**attributes** such as `world` and `character` give a thin wrapper to directly, and easily access parts of the database. While `character_helper_methods` give away what they do, I hope.

It also supports runtime re-loading! Simply add the new helper modules to the `__all__` list (the name of the file without extension) inside `__init__.py` to add it to the loaded/reloaded modules. Keep in mind this merely loads/reloads them and little else, in order to have them available in the `Database` class, modify its `__init__` method with the appropriate instantiation and reference grabbing. (see the source code of `__init__.py`)

##### Helper methods?

Python modules such as `character.py` and `world.py` each implement a class under the same name (plus the CamelCasing) that hold a reference to the thin wrapper they help with (like `character` property of the database class in the case of `character.py`)

Everything else is.. well.. things to help with operations. Please see either `character.py` or `world.py` to see how they work. Really, they have nice understandably named methods in there, go read!

#### owo Whats this `datatypes` folder?

Why don't you open it and find out?

---

### Extending

##### With a new database/collection

1. Simply go inside `__init__.py` and under the `Database` class variables add a reference to the database name and/or collection name (ensure class variable names start with two underscores `__`).
1. Under the `__init__` method of the `Database` class add a reference to the database/collection that was newly added **ENSURING A NICE AND UNDERSTANDABLE NAME** (this is a thin wrapper as we call it).

Now thats a bit convoluted just to add a reference to a database/collection. However, using a class variable allows for easily finding the names of the database/collection in code. (also its consistent through all the classes so you can change it at runtime if something spooky happened)

Adding a reference to the database/collection on the other hand merely shortens and makes it less error-prone to access certain collections of the database. (just look at the character collection)

##### With a new collection of Helper methods

1. Make a new python module with the name of your choice (please be sensible)
1. Inside this new module, implement a new class that has an `__init__` method that takes a reference to the database/collection it works on.
1. Write the helper methods inside this class.
1. Add the filename (without extension) of the new python module to the `__all__` list inside `__init__.py`
1. Instantiate and grab a reference to this new and awesome collection (really, just an object) of helper methods. (using the naming scheme of `somethind_helper_methods` makes it verbose, especially if `something` is allready used as the thin wrapper for the raw database operations)

After loading/re-loading the database package the changes should propagate! And done!