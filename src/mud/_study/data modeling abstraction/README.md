As far as I've seen there are three ways most common that data is modelled in databases, these are respectively:

* key-value
* Document object
* Graph

In this experiment I will try emulating all three types of data-modelling with just one, and provide as simple an interface as possible.

The simplest and most flexible of these, the Document object storage, will be selected for this as many NoSQL databases exist and even the internet is built on sharing documents in the shape of JSON.

So JSON is good! And JSON is a Document essentially. Also python Dictionaries can act like JSON and have nice mechanics to switch to and from Dictionaries and JSONs.

---

## Synopsis of experiment

#### Key-Value storage
