In this study. I'll look at the possibility of enforcing types and validating variable input during value setting.

This is an incredibly important feature for game development, as the flexibility of python classes, while incredible during development, will be a nightmare later on when a crafty developer will later come along and start modifying them at runtime, or when someone makes a typo and all silently will go through to the database in the background.

For this reason I'll look into implementing the descriptor pattern (as seen here: <https://docs.python.org/3/howto/descriptor.html>) and possibly using the `traitlets` package which hopes to solve just this issue, being more mature as it is used extensively in the Jupyter and IPython projects.

---

### Conclusion

The best solution is the more manual wrapper class. (see class `Wrappee` and `Wrapper`)

This gives the benefits of traitlets while abstracting away the incredible amounts of methods inherited by the necessary base class.

If at all possible, this solution is the best one I have found and should be used, potentially writing a script to auto-generate the wrapper classes outside of runtime would help coders.

The main advantage which we do not want to discredit, is that this allows the dot syntax, IDE code completion and so on that other solutions do not, as such developing with these is preferable.

---

### Working with traits

As seen in the code example, writing and using traits is quite easy (see the classes `Ascii` and `Traditional`) and allows for extending their functionality and value validators not by overriding them, but by adding another layer of validation.

##### the downside

Unfortunately, this adds a plethora of methods to the class (see an instance of `Traditional`) that will appear to the developer, which may not be desirable as it clutters the classes we work with, and sometimes we need to even restrict access to such. We do not want to add extra fields to existing data structures at runtime if it is being synchronised to a database, after all.


### Hiding the messy bits with a one class per trait pattern

This has the advantage of hiding all the methods and presenting a more uniform access that is not tied to re-writing classes. (see `CompName`, `CompLevel`, `Compartmentalized`)

##### the downside

It hides all accessible traits from the IDE and also hides all the documentation we have put out in to it. So it is hard to develop with it. Not recommended.

### Hiding the messy bits with a tediously made wrapper class

The traited class is developed normally and then a wrapper class is written using the `@property` and `@propertyname.setter` decorators to limit access to them.

This has the benefit of allow introspection in the IDE and having the desired limit, while still allowing access to the wrapped up class if necessary.

##### the downside

It is tedious and repetitive to write, possibly needing a script to generate it once the main class has been developed to prevent errors in writing it.

It also does not have the documentation the main class would have, necessitating copy-pasting it to this new wrapper class.

However this works and works well once made.

### Doing it from scratch

It takes considerable, time, effort, skill and testing to ensure the written traits work correctly. (see <https://docs.python.org/3/howto/descriptor.html> for how to do it)

This works well compared to traits once it is made.

(see classes `DescAscii`, `DescInt`, `Descriptorized`)

##### the downside

You cannot easily extend validation logic. In fact necessitating re-writing it from scratch every time some change is needed or some variation on the class is needed.

It is haaard to get it right, and need to catch many of the errors and display them.

This is not at all recommended as it is not easily extendible.