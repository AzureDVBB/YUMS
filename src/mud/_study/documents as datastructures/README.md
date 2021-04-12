In python we already have mechanisms for storing structured data with a dictionary, which can also be stored on disk (in plain text via json files) and on databases which are specialized for the storage and retrieval of json data (called documents).

However there are certain downsides in using dictionaries in python for the storage and manipulation of game data:

* Dictionaries lack IDE introspection, that is you do not know what value, or even what key lives inside of them unless tested, thus most IDE's will have difficulty giving hints.
* As with all variables in python, dictionary values are not typed. Thusly it requires care when handling the data in code that accesses and/or changes it.

---

The proposed solutions here addresses both points with using `traitlets` as a new dependency.

`traitlets` is a module for enforcing class attribute correctness, not just in type but in values as well.

It introduces class attribute object that enforces types (Int, Str, Float, etc.) and gives mechanisms to write custom type objects. It also provides a way to validate the new values that the user tries to set, so that only correct values will be accepted. Finally it also provides the ability to write callback functions for each of these attribute objects, so when an attribute is successfully changed, a user defined function is run to produce some desired side-effect.

For more information on `traitlets` see their documentation at <https://traitlets.readthedocs.io/en/stable/using_traitlets.html>

In this mock-up A persistent document storage method has been created. The document objects need to inherit the `PersistentDocument` abstract base class. They also need to define their own `__init__` method and `_filename` property to work correctly. They then can define and implement their own list of traits that will then be persisted onto disk.

These `PersistentDocument`s are then accessed in the same manner as dictionaries (thanks to the base class implementing `__setitem__` and `__getitem__` methods). The object then acts like a read-cache, refreshing itself by reading from disk every 10s after the last read, but only when the object is accessed. Additionally every time the object has one of it's values set, the entire object is written to disk in JSON format, overriding existing files.

The caveat is that because we use `__setitem__` and `__getitem__` the functions to deal with diskIO will only fire if we use the `document[key]` notation to access the attributes, the `document.key` notation works too but it bypasses it.

A workaround would be to use the `@observe` decorator to have callbacks on changes, this works instead of `__setitem__` but the `__getitem__` has no such workaround as far as I have seen.

---

#### Summarized

`traitlets` provide elegant and robust ways to strictly enforce object attribute type correctness, while also going one step further to allow for checking value validity before setting and also provides the option to write callback functions to react to changes.

In here is an example on how to combine `traitlets` with `__setitem__` and `__getitem__` object methods in order to create an abstraction layer for an underlying data storage with strict type and value checking, while providing similar interface to a python **dictionary**. It also provided a caching solution to reduce diskIO operations and invalidates itself after 10s to ensure the values stored in the object reflect the persistent storage.

However access cannot be limited to use `document[key]` only and the `document.key` notation is accepted but bypasses the `__setitem__` and `__getitem__` methods.

#### Further Exploration

Further exploration in time-invalidated caching wrappers is needed to reduce server strain on frequently accessed data. Similar to `lru_cache` decorator if at all possible.

Additionally, how to access object attributes with the `object.attribute` notation without the superfluous methods being visible in the IDE should be looked into. **(See the study `_study/traitlets for strict attributes` for this)**