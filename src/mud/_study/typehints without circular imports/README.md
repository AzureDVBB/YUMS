To help with development and enable tab completion in our IDE's of choice, type hinting is near essential tool to inform said IDE about the object and its methods.

To facilitate this even in classes that import each other, which would cause ``Circular Import Error`s, the typing module adds the flag `TYPE_CHECKING`.

Simply put: If you only import things to use in type hinting then use the following scheme to do your import statement.

```
python

if TYPE_CHECKING:
	from foo import bar  
```

**Note:** this will be picked up by IDEs (tested with Spyder-IDE using Kite) for code hinting, so it is super useful if only for that.