#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2024-12-19T21:07:16-05:00

@author: nate
"""

import DictOnly

def test_main():
    my_tree = {
        1: [1,1,3,4,5],
        5: {
            "x": [1, 2, 3],
            "y": [4, 5, 6]
        }
    }

    tree0 = DictOnly.DictOnly(my_tree)

    assert tree0.get(1, 0) == 1
    assert tree0.get(5, 'x', 2) == 3
    assert tree0.get(5, '123', 1, 2, 3, 4, default=777) == 777
    tree0.set(5, '123', 4, val=777)
    assert tree0.get(5, '123', 4) == 777
    tree0.set("_1", '_2', "_3", "_4", val=777)
    assert tree0.get(5, '123', 4) == 777
