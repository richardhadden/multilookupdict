# Multi-Lookup-Dict

A Dict-like container that allows multiple keys to address the same value.

```python
>>> d = MultiLookupDict()
>>> d["a_key"] = "some_value"
>>> d.map_key("a_key", "another_key") # Make "another_key" an alias of "a_key"

```
Implemented as two dicts:
    - `MultiLookupDict._data` holds the 'canonical key' and value
    - `MultiLookupDict._key_to_canonical_map` maps 'alias keys' onto canonical keys.
        (Canonical keys are mapped to themselves in this dict)
        
Externally, all keys (canonical and alias) are treated identically,
and all refer to the same value, unless a key is reassigned to another value using `map_key`.


Multi-key lookups and assignments
---------------------------------

Iterables of keys can also be accessed, set, and mapped.

```python
>>> d = MultiLookupDict()
>>> d[("key_a", "key_b", "key_c")] = "some_value"
>>> d["key_a"] == "some_value"

Where items are accessed with multiple keys, all distinct matching values are returned
as a list (where multiple keys are requested, the result is always a list, for consistency)

>>> d["key_d"] = "some_other_value" # Add a distinct value
>>> d[("key_a", "key_b", "key_d")] == ["some_value", "some_other_value"]


>>> d.map_key("key_a", ("key_e", "key_f")) # Also do multiple mappings
```

...

Methods
-------

__setitem__
    Sets a key to the value. If a (non-string) iterable is provided
    as key, each key will be assigned the value.
__getitem__
    [As with standard Python dict]
map_key
    Assign the value of one key to another key. Both keys
    now point to the same value.
keys
    Returns all keys in MultiLookupDict. Returned keys refer to same or different objects.
all_keys
    [Same as `keys`]
values
    [Same as `dict.values`]
items
    Same as `dict.items`, except key part of tuple is a `set` of keys for the corresponding value
pop
    Same as `dict.pop`. All keys pointing to value are removed.
aliases
    Returns all aliases of a given key