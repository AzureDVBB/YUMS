# backend agnostic DocumentDB

Now with a few ***GRAPH*** functionalities!

## pre-ramble (AKA: setting our goals and expectations)

In this little experiment I will try to create the impossible, yet seemingly feasible, Document oriented DB backend that will not care about what backend we decided to use. 

In this way we would not only abstract away the underlying database implementation, but also allow developers to later on pick their preferred database backend and driver, only needing to write a connector to be used.

While yes some would cry out amidst the layers of abstraction `"where can I put my meticulously written queries?!"` fret not! For you forget we are in the land of the *python*. One of our key principles is to give you every tool and only hide what we absolutely must, so you will have direct access to the database backend driver if you so choose to take advantage of it.

Granted this is actually not advised for a project such as this **YUMS** mud framework.

Why? Well you see, not everyone on your team will want to also learn the specific data query magic necessary to accomplish even the most simple of tasks such as getting a document, getting a specific data from a document, updating it etc.

Do try to remember, abstractions are there to simplify otherwise complicated operations so that even Dave down the hallway can use it correctly every time, and not accidentally corrupt your carefully maintained database with a dirty query.

Finally it will allow us to use the same API to interact with a lightweight test database as well as a massive cloud based one distributed along the globe! That would allow us to simply test and verify all functionality offline and then have it (hopefully) not break when it goes live.

## Dictionary <---> Document

Documents can be really easily be modeled in python with dictionaries. The same access patterns, key-value pairs and.. well okay they are JSON and we will convert between the two with a built-in package.
This has already been explored in `code_playground/Data Storage/documents as datastructures/`

This time however we will deal with the specific implementation of mapping a dictionary into a document in a persistent store. Crucially there are a couple of concepts that are necessary and I refuse to let go, just based on how useful it is and will be in this project's development and maintenance:

* dictionary-like front end
* schema and data validation (with traitlets)
* migrations and and schema versioning
* 