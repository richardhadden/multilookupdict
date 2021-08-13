# Multi-Lookup-Dict

### A `dict`-like container that allows multiple keys to address the same value.
<br/>

## Installation

`pip install multilookupdict`


## Usage

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
```
Where items are accessed with multiple keys, all distinct matching values are returned
as a list (where multiple keys are requested, the result is always a list, for consistency)
```python
>>> d["key_d"] = "some_other_value" # Add a distinct value
>>> d[("key_a", "key_b", "key_d")] == ["some_value", "some_other_value"]


>>> d.map_key("key_a", ("key_e", "key_f")) # Also do multiple mappings
```



Methods
-------

<dl>
<dt>
<code>__setitem__(key/iterable_of_keys, value)</code>
</dt>
    <dd>Sets a key to the value. If a (non-string) iterable is provided
    as key, each key will be assigned the value.</dd>
<dt><code>__getitem__(key/iterable_of_keys)</code></dt>
    <dd>Gets a value from a key. If a (non-string) iterable is provided as a key, a list
    of distinct values matching all provided keys will be returned.</dd>
<dt><code>map_key(existing_key, new_key)</code></dt>
    <dd>Assign the value of one key to another key. Both keys
    now point to the same value.</dd>
<dt><code>keys()</code></dt>
    <dd>Returns all keys in MultiLookupDict. Returned keys refer to same or different objects.</dd>
<dt><code>values()</code></dt>
    <dd>[Same as <code>dict.values</code>]</dd>
<dt><code>items()</code></dt>
    <dd>Same as <code>dict.items</code>, except "key" part of the tuple is a <code>set</code> of keys for the corresponding value</dd>
<dt><code>pop(key)</code><dd>
    <dd>Same as <code>dict.pop</code>. All keys pointing to value are removed.</dd>
<dt><code>aliases(key, omit_requested_key=False)</code></dt>
    <dd>Returns all aliases of a given key, including the key provided. (Set <code>omit_requested_key</code> to <code>True</code> to exclude the provided key.)</dd>
</dl>