import pytest
from bson import ObjectId
from src.utils.format_perfume_id import format_perfumes_ids, format_perfume_id


def test_format_perfume_id_transforms_id():
    obj_id = ObjectId()
    perfume = {"_id": obj_id, "name": "Perfume X"}

    formatted = format_perfume_id(perfume)

    assert "id" in formatted
    assert formatted["id"] == str(obj_id)
    assert "_id" not in formatted
    assert formatted["name"] == "Perfume X"


def test_format_perfumes_ids_multiple_items():
    ids = [ObjectId() for _ in range(3)]
    perfumes = [{"_id": oid, "name": f"Perfume {i}"} for i, oid in enumerate(ids)]

    formatted = format_perfumes_ids(perfumes)

    assert len(formatted) == 3
    for i, perfume in enumerate(formatted):
        assert perfume["id"] == str(ids[i])
        assert "_id" not in perfume
        assert perfume["name"] == f"Perfume {i}"
