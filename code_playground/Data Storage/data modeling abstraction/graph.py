#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 22:55:21 2021

@author: AzureDVBB
"""

from document import Document

class Graph:

    _nodeCollections: list[str]
    _edgeCollection: str

    def __init__(self, graphname: str, node_collections: list[str]):
        self._edgeCollection = graphname+'-edges'
        self._nodeCollections = node_collections

    def get_document_edges(self, collection: str, key: str):
        pass

