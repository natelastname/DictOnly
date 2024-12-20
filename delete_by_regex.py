#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2023-11-04T09:29:34-04:00

@author: nate
"""
import json
import requests
import argparse
import sys
import os
import itertools
import tqdm

from typing import Optional
from typing import Union
from pydantic import BaseModel
import pydantic

from pydantic import BaseModel, Field, ValidationError

from opensearchpy import OpenSearch

######################################################################

host = 'localhost'
port = 9200
auth = ('admin', 'admin')

os_client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False
)
######################################################################
import json5
import itertools

class DictOnly:
    tree = None
    def __init__(self, obj, **kwargs):
        self.tree = self._load(obj)
        return

    def _load(self, obj):
        if isinstance(obj, dict):
            gen0 = obj.items()
        elif isinstance(obj, list):
            gen0 = enumerate(obj)
        else:
            return obj
        
        result = {}
        for key, val in gen0:
            result[key] = self._load(val)

        return result

    def get(self, keys, default=None):
        subtree = self.tree
        for key in keys:
            if not isinstance(subtree, dict):
                return default
            if not key in subtree:
                return default
            
            subtree = subtree[key]
        
        return subtree

    def get(self, *keys, default=None):
        subtree = self.tree
        for key in keys:
            if not isinstance(subtree, dict):
                return default
            if not key in subtree:
                return default
            subtree = subtree[key]
        return subtree
    
    def set(self, *keys, val=None):
        subtree = self.tree
        done_sym = object()
        
        i0 = itertools.chain(keys, [done_sym])
        
        key = next(i0)
        while key != done_sym:
            next_key = next(i0)
            
            if not isinstance(subtree, dict):
                raise KeyError(keys)
            elif not key in subtree and next_key == done_sym:
                subtree[key] = val
                return
            elif not key in subtree:
                subtree[key] = {}
            
            subtree = subtree[key]
            key = next_key
        return

    def __setitem__(self, keys, val):
        return self.set(keys, val)
    def __getitem__(self, args):
        return self.get(args)
    def __iter__(self):
        return self.tree.__iter__()
    def keys(self):
        return self.tree.keys()
    def values(self):
        return self.tree.values()
    def itervalues(self):
        return self.tree.itervalues()

            
my_tree = {
    1: [1,1,3,4,5], 
    5: {
        "x": [1, 2, 3],
        "y": [4, 5, 6]
    }
}
tree0 = DictOnly(my_tree)
assert tree0.get(1, 0) == 1
assert tree0.get(5, 'x', 2) == 3
assert tree0.get(5, '123', 1, 2, 3, 4, default=777) == 777
tree0.set(5, '123', 4, val=777)
assert tree0.get(5, '123', 4) == 777
tree0.set("_1", '_2', "_3", "_4", val=777)
assert tree0.get(5, '123', 4) == 777
######################################################################



stats = os_client.indices.stats()
indices = stats['indices']
filtered = {}
for index_name in indices:
    if index_name.startswith('.'):
        continue
    tree0 = DictOnly(indices)
    total = tree0.get(index_name, 'total', 'docs', 'count')
    if total == None:
        breakpoint()
    
    print(f"{index_name} - {total}")
    if total <= 100:
        resp = os_client.indices.delete(index_name)
        if resp['acknowledged']:
            print("Deleted")
        else:
            breakpoint()
            
