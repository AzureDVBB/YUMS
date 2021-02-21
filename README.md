# YUMS
Yet Another MUD Server (now with a typo!)

## CAUTION
This is still heavily **In Development** and as such things can and will change drastically.
As such, use this as the foundation of your own projects **at your own risk**.
(Even if this is just a bare-bones implementation that the user is expected to build, hack and change to their needs.)

## what 'exactly' is it?

A MUD (or Multi User Dungeon) is an online (usually) text-based game. Think of them like the first MMO's out there, before fancy graphics were a thing. Got a terminal and an internet connection? That's all you needed. Want to learn about that history? Head on over to <https://en.wikipedia.org/wiki/MUD>, yes really.

---

##### The rambling about it (the background, you may skip this freely)

In that vein I, the github user known as AzureDVBB, have searched for frameworks and packages for Python to create just such a MUD. There was a few, but each had it's own issues. Here are some honorable mentions (that are well worth a checkout).

<https://github.com/evennia/evennia> is an absolutely amazing project, it's a MUD that's absolutely batteries included. However because it is batteries included... would necessitate weeks of chewing through to understand. As such, for me personally the barrier to entry was high, especially with the usage of twisted and django.. It was just daunting for me.

<https://github.com/Frimkron/mud-pi> is a teeeny tiny mud, honestly one of the main reasons why I chose to attempt writing my own. But it has two flaws. It's too simple and... it uses raw sockets. Thats incredibly low-level.

However digging in the newer python versions I have found the jackpot, exactly what was needed to create a simple MUD server, namely, streams <https://docs.python.org/3/library/asyncio-stream.html>.

This just hands down gave the simplest MUD server with the example, which worked with all MUD clients out of the box. Incredible. Everything else was built around the examples found within.

## The actual answer (finally!)

The **YUMS** repository is a hackable MUD server implementation using Python 3.8+ `asyncio` library to implement it a web server with python natively, alongside the concurrency of async programming.

**It however, is little more then a barebones core, with minimal functionality to demonstrate and show how a MUD server can work and to provide a codebase to extend into an actual game.**

It's only dependency is `motor` which is an async database driver for the database of choice `Mongo DB` for the sole reason that it's both flexible and performant.

The repository is not here to appear as a package on PyPI, to import and include into python code, but more of a project to copy/fork, hack and bend to one's will. Or learn more about how asyncio works (i don't know how it works, its all black magic, I merely know the magic words).

## Requirements

`Python 3.8+` (developed with 3.8.5)

`motor` (developed with 2.2.0)

To get the only requirement `pip install motor`, for more information about it check out <https://github.com/mongodb/motor>

**The catch** is it needs a running `Mongo DB` server to connect to. Head on over to it's website and install it if possible, at <https://www.mongodb.com/try/download/community>

If however, one cannot install MongoDB on the computer of choice (like me because Arch Linux and a refusal to use AUR packages for it) there is another option...

Using **docker** containers to neatly sandbox them in... containers.. its magic don't worry. I was using docker soo...

Here are convenient "i don't know what I'm doing but I need it" steps to get you started (like I did) with running Mongo DB with docker.

---
**Caution: Skip this if there is a MongoDB server somewhere you can connect to, or installed it like a sane person.**

To get MongoDB running in docker (once you have it installed) first run the command `docker pull mongo` this will pull the latest docker image of MongoDB.

Next run `docker run --name insert_name_here -p 27017:27017 -d mongo` which will create a container with the name `insert_name_here` (please use something sensible and without spaces) so we can refer to it by name. The argument (is spooky dangerous in production, but playing around it's fine) `-p 27017:27017` which lets us access the database from outside the container. `-d mongo` specifies the container we use as the official Mongo DB container.

Now we (hopefully) have a running database. We can stop it with `docker container stop insert_name_here`. And start it back up with `docker container start insert_name_here`. Yes we do want to start it back up as we need the data inside to be persistent yeah?

We can also delete the container with `docker container rm insert_name_here` (deleting the database along with it most likely.)

**Do note** that I will be sad and won't help you diagnose docker. Or help you with it for that matter. It's black magic and you are on your own. I merely listed commands I use so I can remember it years from now.

## Documentation

You are reading it. Every folder has a README like this inside. Most of the code is easily readable and/or commented, some even has docstrings! 

Feel free to just click around and poke into things, that's how it was intended to be used, hence the non-standard documentation format. After all, one must know how it works to bend it tho their will.

## Contributing

There's the github issues for that but please.. only put issues on the following topics:

* Documentation issues, inconsistencies and requests/enhancements
* Bugs in the code
* Performance enhancements
* Tests to measure said performance and enhancements (and/or stress testing)

This is a barebones base for others to learn from and expand upon to build their own things, please do not request MUD commands or mechanics to be added to this core.

Have some awesomeness that you just made to improve upon the source code? Submit a pull request!

No I don't know how any of it works, I'm new here! - 2020/08/25

