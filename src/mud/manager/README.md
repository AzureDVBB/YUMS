### The Many Managers managing the MUD

If it needs to store data, if it needs to provide interaction or if it needs to store state and provide complex mechanics? You have come to the right place!

##### So what is it?

It's a bunch of regular python classes implementing any and all complex systems that require, for instance an internal state that needs to be kept up-to date and provide ways of manipulating it. (see `player.py` for an excellent example on how the `move` needs to update internal state.)

It is also a way to neatly separate out parts of the MUD code, while still allowing them access to other such managers through the main `Manager` class. Why? Because they all get a reference to it!

Won't this cause some circular import nonsense issue? No thanks to only importing stuff during the special initilaization method inside the main `Manager`.

##### But why so seperated and reference passed?

In short, read about proxy objects at <https://docs.python.org/3/library/multiprocessing.html#proxy-objects> which will be rather convenient once certain managers and/or functions outgrow a single python process. (*cough* multiprocessing *cough*) 

As I hope this would be a much simpler change with this level or separation/reference passing.

---

### Extending

1. Make a new module/package and implement a class inside it (preferably named like `SomethingManager`)
1. Inside it's `__init__` method, make sure it accepts atleast a reference to the main manager (see existing modules for examples)
1. Change `Manager.initialize_inside_running_loop` method inside `__init__.py` to import the newly created manager class and then instantiate it, grabbing a reference as an attribute (just look in `__init__.py` to see this in action)

Note: This is how you will then access the new manager, so chose the name wisely.

Also note: Complete python restart needed to see changes.