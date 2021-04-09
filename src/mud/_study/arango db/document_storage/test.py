#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 12:56:20 2021

@author: AzureDVBB
"""

import arango

# connect to the hosted database (URL should point to the database, or the coordinators in a cluster)
db_url = "http://localhost:8529"
client = arango.ArangoClient(hosts=db_url)

# connect to the default "_system" database as a user (in this case the root user)
sys_db = client.db("_system", username="root", password="")

# create a new "test" database
sys_db.create_database("test")

# connect to the new database
db = client.db("test", username="root", password="")

# create a new document collection
col = db.create_collection("coll")

# insert a document into the collection
col.insert({"name": "testing", "number": 1})

# retrieve a documents fitting a filter (resulting is a cursor)
cursor = col.find({"name": "testing"})

# retrieve a batch of documents from a cursor (originally returns a deque object)
docs = list(cursor.batch())

print(docs[0])

# update a document
document = docs[0]
document["number"] = 2

col.update(document)

print(col.find({"name": "testing"}).batch()[0])

# delete a database (and associated python references)
sys_db.delete_database("test")
del db, col, cursor, document, docs

