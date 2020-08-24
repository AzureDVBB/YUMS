# Welcome to the heart of the MUD

Here there be dragons I hope! (I love dragons...)

### Folder structure and explanation

In no particular order the folder structure is as follows.

* **commands** holds the main command interpreter that processes player inputs and returns the output to them. It has access to the `database` by its own object instance and `manager` by passed reference.
* **database** holds a wrapper class for the MongoDB client connection. It has both thin wrappers exposing the `motor` package API directly on databases/collections as well as helper methods to abstract away complex or often used database operations.
* **manager** holds classes that manage in-memory MUD operations and complex systems that need to keep track of, and handle their internal states. It has it's own `database` connection, while instantiating the `commands` interpreter in a manager. (and passing itself as reference to it)
* **_study** which holds sketches, studies and mockup implementations of several systems/tricks used in the creaton of this package.

### The two other python files?

##### `connection.py`

houses the `Connection` class (surprise) which handles the raw read/write streams of connected clients. Basically it awaits an input from a client, decodes it and puts it into a `read_queue`, while also awaiting items to be put into it's `write_queue` which it then encodes and send it to the clients as output. This is 2 asynchronous tasks running concurrently for each connection.

In addition it holds a few more information about itself: 

* `is_alive` which is True while the client is still connected, however False if it died. Setting this attribute to False however will disconnect the client regardless.
* `address` which holds the IP address and port of the connected client.
* `reader` and `writer` for low level access to the input/output streams, more information about them can be found here: <https://docs.python.org/3/library/asyncio-stream.html>

##### `server.py`

This is the main entry point of the entire MUD, yet it is exceedingly simple and small.

All it really does is start up an event loop (for asyncio), initialize the `manager` inside the running loop, and then start the server that runs forever.

Additionally it has a callback for the server to call whenever a new connection is recieved. In this case it will immediately calls for the manager to authenticate the connection.

The only function that needs to be run to start the server up however is `run()`

##### wait... `run()` ?

That's right, a function is there to run the server. Why? Well, in order for relative/absolute imports to work throughout the entire package, it needs to be imported as such. This means that the top level `__init__.py` will run and then run all modules, producing side effects if not held in function and/or class definitions. 

As such, a function to start the server needs to written and used to avoid such side effects.

This however means that the entire MUD needs to be imported and then `mud.run()` called.