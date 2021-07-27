# Multi-Lookup-Dict

A Dict-like container that allows multiple keys to address the same value.

```
    >>> d = MultiLookupDict()
    >>> d["a_key"] = "some_value"
    >>> d.map_key("a_key", "another_key") # Make "another_key" an alias of "a_key"
```
Implemented as two dicts:
    - `MultiLookupDict._data` holds the 'canonical key' and value
    - `MultiLookupDict._key_to_canonical_map` maps 'alias keys' onto canonical keys.
        (Canonical keys are mapped to themselves in this dict)

Externally, all keys (canonical and alias) are treated identically,
and all refer to the same value, unless:
- a key is reassigned individually with a new value using `__setitem__`
- a key is reassigned to another value using `map_key`

...

Methods
-------

`__setitem__`
    Sets a key to the value. If a (non-string) iterable is provided
    as key, each key will be assigned the value.
`__getitem__`
    [As with standard Python `dict`]
`map_key`
    Assign the value of one key to another key. Both keys
    now point to the same value.
`keys`
    Returns all keys in MultiLookupDict. Returned keys refer to same or different objects.
`all_keys`
    [Same as `keys`]
`values`
    [Same as `values`]