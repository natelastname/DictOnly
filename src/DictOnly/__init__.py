#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2024-12-19T21:07:16-05:00

@author: nate
"""

import sys
import os
import itertools
import json5


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

    def dumps(self, **kwargs) -> str:
        return json5.dumps(self.tree, **kwargs)

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
