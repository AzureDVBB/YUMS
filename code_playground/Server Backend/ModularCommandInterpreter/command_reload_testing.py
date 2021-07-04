import importlib

import time

import commands

interpreter = commands.Interpreter()
interpreter.process("example1", "test")
interpreter.process("example3", "test")

print("waiting 30s before reloading and next run.... please change the user/admin_level \
example files to see the effects.")
time.sleep(30)
importlib.reload(commands)

interpreter = commands.Interpreter()
interpreter.process("example1", "test")
interpreter.process("example3", "test")