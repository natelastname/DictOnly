========
DictOnly
========

    :Author: nate
    :Date: 2024-12-19



1 Introduction
--------------

``DictOnly`` is a Python module for systematically manipulating
complicated and/or unpredictable "JSON" data structures (i.e., objects
consisting of arbitrarily nested dictionaries and lists.)

The basic idea is to convert lists to dictionaries so that both
objects can be handled in the same way. For example, the list

::

    [
      "item1",
      "item2",
      "item3"
    ]

is transformed into the dictionary

.. code:: json

    {
      "0": "item1",
      "1": "item2",
      "2": "item3"
    }

2 Example 1
-----------

The goal is to get ``response['key1']['key2']['key3']`` without assuming:

1. ``response['key1']`` exists and is a dictionary

2. ``response['key2']['key2']`` exists and is a dictionary

3. ``response['key1']['key2']['key3']`` exists and is a dictionary

One obvious solution to this problem would be

.. code:: python

    def handle_response(response):
        tmp = response
        # Get key1 if it exists
        tmp = tmp.get('key1')
        if not tmp:
            return
        # Get key2 if it exists
        tmp = tmp.get('key2')
        if not tmp:
            return
        # Get key3 if it exists
        tmp = tmp.get('key3')
        if not tmp:
            return

        return tmp

Using DictOnly, this becomes

.. code:: python

    import DictOnly

    def handle_response(response):
        tree = DictOnly.DictOnly(response)
        return tree.get('key1', 'key2', 'key3')

3 Example 2
-----------

Here's an example borrowed from ``test/test_main.py``:

.. code:: python

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
