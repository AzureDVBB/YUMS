#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 11:21:05 2020

@author: AzureDVBB
"""
import asyncio

import motor.motor_asyncio as motor # import the ASYNCIO motor
import pymongo

# before anything, start up a mongodb server, this assumes a standard 'mongo' docker
# image is running on the standard port
# You can connect to any mongodb server running by changing the URI


# no I/O is needed for any of these (metadata?) so DO NOT await
# create client connection to dbserver
# client = motor.AsyncIOMotorClient('mongodb://localhost:27017') # asyncio client
client = pymongo.MongoClient('mongodb://localhost:27017') # normal sequential client

db = client.test_db # grab a reference to the database 'test_db' from the server
db = client['test_db'] # same as above except with a different notation, this is way easier to name

collection = db['test collection'] # get a collection (of documents) reference



# I/O operations, use AWAIT with each one of these database calls
collection.insert_one({'name': 'test', 'value': 12}) # insert a document(dictionary) into collection


print(collection.find_one({'name': 'test'})) # find and print one document with 'test' as name