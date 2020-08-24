### The support package for manipulating text!

Now with runtime re-loading support!

##### The simplest

This is merely a package holding useful text formatting functions to not clutter up other parts of the code, or to make it consistent across all of the MUD.

Implement things here if there is a need for text formatting elswhere in the MUD for input/output text.

### Extending

##### New function in existing module

Merely load/re-load the package and the changes will propagate.

###### New module

Add the new module file name (without extension) to the `__all__` list inside `__init__.py` and then load/re-load the package for changes to propagate.