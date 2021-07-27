from collections import defaultdict
from collections.abc import Sequence, KeysView, ValuesView


def _is_sequence(val):
    return (isinstance(val, Sequence) and not isinstance(val, str)) or isinstance(
        val, (KeysView, ValuesView)
    )


"""
TODO:  implementation of standard dict methods:
    - pop
    - del
    - clear
    - copy
    - fromkeys 
    - get 
    ✅ items
    ✅ keys 
    - pop
    - popitem 
    - setdefault
    - update
    ✅ values

"""


class MultiLookupDict:
    """
    A Dict-like container that allows multiple keys to address
    the same value.

    >>> d = MultiLookupDict()
    >>> d["a_key"] = "some_value"
    >>> d.map_key("a_key", "another_key") # Make "another_key" an alias of "a_key"

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
        [Same as `values`]
    """

    def __init__(self, values={}):
        self._data = {}
        self._key_to_canonical_map = {}
        for keys, value in values.items():
            self.__setitem__(keys, value)

    def _set_single_name_and_value(self, key, value):
        """Sets a single key and value."""
        if key not in self._key_to_canonical_map:
            self._key_to_canonical_map[key] = key

        self._data[self._key_to_canonical_map[key]] = value

    def __setitem__(self, key, value):
        if _is_sequence(key):
            self._set_single_name_and_value(key[0], value)
            for k in key[1:]:
                self.map_key(key[0], k)
        else:
            self._set_single_name_and_value(key, value)

    def __getitem__(self, name):
        try:
            return self._data[self._key_to_canonical_map[name]]
        except KeyError:
            raise KeyError(f"Key '{name}' not found")

    def __contains__(self, name):
        return name in self._key_to_canonical_map

    def _canonical_to_all_keys(self):
        """Gets all keys associated with a canonical key"""
        key_map = defaultdict(list)
        for ref, can in self._key_to_canonical_map.items():
            key_map[can].append(ref)
        return key_map

    def map_key(self, existing_key, new_key):
        """Assigns the value of an existing key to another key."""

        if existing_key not in self._key_to_canonical_map:
            raise KeyError(f"Existing key '{existing_key}' not found")

        self._key_to_canonical_map[new_key] = self._key_to_canonical_map[existing_key]

    def keys(self):
        return self._all_keys()

    def all_keys(self):
        return self._key_to_canonical_map.keys()

    def canonical_keys(self):
        """This is a nonsense! They might have escaped from under us!"""
        return self._data.keys()

    def __iter__(self):
        yield from self.keys()

    def items_with_canonical_keys(self):
        return self._data.items()

    def items(self):
        key_map = self._canonical_to_all_keys()
        for canonical_key, value in self._data.items():
            yield key_map[canonical_key], value

    def values(self):
        return self._data.values()
