import pytest

from multilookupdict import __version__
from multilookupdict import MultiLookupDict
from multilookupdict.multilookupdict import _is_sequence


def test_version():
    assert __version__ == "0.1.0"


def test_can_init_with_no_args():
    d = MultiLookupDict()
    assert d._data == {}
    assert d._key_to_canonical_map == {}


def test_init_from_single_key_dicts():
    d = MultiLookupDict({"one": "one_value", "two": "two_value"})
    assert d._data == {"one": "one_value", "two": "two_value"}
    assert d._key_to_canonical_map == {"one": "one", "two": "two"}


def test_init_from_multi_key_dicts():
    d = MultiLookupDict({("one", "two"): "v1", "three": "v3"})
    assert d._data == {"one": "v1", "three": "v3"}
    assert d._key_to_canonical_map == {"one": "one", "two": "one", "three": "three"}
    assert d["one"] == "v1"
    assert d["two"] == "v1"
    assert d["three"] == "v3"


def test_set_item_with_single_key():
    d = MultiLookupDict()
    d["thing"] = "thong"
    assert d._data == {"thing": "thong"}
    assert d._key_to_canonical_map == {"thing": "thing"}


def test_set_item_with_multiple_keys():
    d = MultiLookupDict()
    d[("thing1", "thing2")] = "thong"
    assert d._data == {"thing1": "thong"}
    assert d._key_to_canonical_map == {"thing1": "thing1", "thing2": "thing1"}

    d["thing2"] = "updated"
    assert d._data == {"thing1": "updated"}
    assert d._key_to_canonical_map == {"thing1": "thing1", "thing2": "thing1"}


def test_get_item_with_single_key():
    d = MultiLookupDict()
    d["thing"] = "thong"
    assert d["thing"] == "thong"


def test_get_item_raises_exception_if_key_missing():
    d = MultiLookupDict()
    with pytest.raises(KeyError) as e:
        d["missing"]
    assert e.value.args[0] == "Key 'missing' not found"


def test_add_key():
    d = MultiLookupDict()
    d["thing"] = "thong"
    d.map_key("thing", "other")

    assert d["other"] == "thong"


def test_set_item_by_mapped_key():
    d = MultiLookupDict()
    d["thing"] = "thong"
    d.map_key("thing", "other")

    d["other"] = "updated"

    assert d["thing"] == "updated"
    assert d["other"] == "updated"


def test_all_keys():
    d = MultiLookupDict()
    d["thing1"] = "thong1"
    d["thing2"] = "thong2"
    d.map_key("thing1", "thing3")

    for k in ["thing1", "thing2", "thing3"]:
        assert k in d.all_keys()


def test_canonical_keys():
    d = MultiLookupDict()
    d["thing1"] = "thong1"
    d["thing2"] = "thong2"
    d.map_key("thing1", "thing3")

    for k in ["thing1", "thing2"]:
        assert k in d.canonical_keys()

    assert "thing3" not in d.canonical_keys()


def test_map_key_to_non_canonical():
    d = MultiLookupDict()
    d["thing1"] = "thong"
    d.map_key("thing1", "thing2")

    assert d["thing1"] == "thong"
    assert d["thing2"] == "thong"

    d.map_key("thing2", "thing3")
    assert d["thing3"] == "thong"


def test_in():
    d = MultiLookupDict()
    assert "something" not in d


def test_canonical_to_all_keys():
    d = MultiLookupDict()
    # This func is internal, should reverse the map...
    d["thing1"] = "thong1"
    d["thing2"] = "thong2"
    d.map_key("thing1", "thing3")
    d.map_key("thing2", "thing4")

    k = d._canonical_to_all_keys()
    assert k["thing1"] == ["thing1", "thing3"]
    assert k["thing2"] == ["thing2", "thing4"]


def test_items_with_all_keys():
    d = MultiLookupDict()
    # This func is internal, should reverse the map...
    d["thing1"] = "thong1"
    d["thing2"] = "thong2"
    d.map_key("thing1", "thing3")
    d.map_key("thing2", "thing4")

    iter_values = [(["thing1", "thing3"], "thong1"), (["thing2", "thing4"], "thong2")]

    for i, (keys, value) in enumerate(d.items()):
        assert iter_values[i][0] == keys
        assert iter_values[i][1] == value


def test_values():
    d = MultiLookupDict()
    d["thing1"] = "thong1"
    d["thing2"] = "thong2"
    d.map_key("thing1", "thing3")
    d.map_key("thing2", "thing4")

    assert list(d.values()) == ["thong1", "thong2"]


def test_is_sequence():
    assert not _is_sequence(1)
    assert not _is_sequence("string")
    assert not _is_sequence(123123.2343)
    assert not _is_sequence({})

    assert _is_sequence([1, 2, 3])
    assert _is_sequence((1, 2, 3))
    assert _is_sequence({"a": 1, "b": 2}.keys())
    assert _is_sequence({"a": 1, "b": 2}.values())


def test_it_does_not_break():
    d = MultiLookupDict()
    d["thing1"] = "value1"
    d[("thing2", "thing3")] = "value23"
    assert d["thing1"] == "value1"
    assert d["thing3"] == "value23"

    d.map_key("thing1", "thing2")
    assert d["thing1"] == "value1"
    assert d["thing2"] == "value1"
    assert d["thing3"] == "value23"
