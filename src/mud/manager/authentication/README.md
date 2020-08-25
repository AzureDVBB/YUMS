# Authentication Manager

Can you log in?

### The short version

This manager is responsible for the verification of user name/password combinations and registration of new users. 

All connections will start here and unless they manage to verify themselves will be force-disconnected after a maximum number of attempts.

### The long version

The authentication is split between two files.

**`password_hasher.py`** houses the logic of hashing passwords, yes. It is running a seperate process to do the actual hashing with some wrapper to allow it to be ran in the main async process. The reason why is this is a computationally expensive function and would block everything else on the server while it works, hence why the seperate process and wrapper.

**`authentication.py`** holds the main manager class that imports and uses the password_hasher. It holds logic for logging a player character in as well as registration of a new one. It also features force disconnection if the connection is unable to authenticate itself.

**`__init__.py`** is required. Also using it to only import the single class that is the actual manager, namely `AuthenticationManager`, thus keeping clean the namespace.