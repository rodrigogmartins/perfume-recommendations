import pytest
from src.perfumes.utils.get_effective_liked_notes import get_effective_liked_notes

def test_merges_liked_and_inferred_notes():
    liked_perfumes = [
        {"all_notes": ["amber", "rose", "jasmine"]},
        {"all_notes": ["amber", "jasmine", "vanilla"]},
        {"all_notes": ["amber", "musk", "jasmine"]},
    ]
    liked_notes = ["patchouli"]

    result = get_effective_liked_notes(liked_perfumes, liked_notes)

    # amber (3x) and jasmine (3x) should be inferred, +1 other (vanilla, rose, or musk)
    assert "patchouli" in result
    assert "amber" in result
    assert "jasmine" in result
    assert len(result) <= 4  # patchouli + 3 inferred
    assert len(result) == len(set(result))  # no duplicates

def test_returns_only_liked_notes_when_no_perfumes():
    liked_perfumes = []
    liked_notes = ["coconut", "lime"]

    result = get_effective_liked_notes(liked_perfumes, liked_notes)

    assert set(result) == {"coconut", "lime"}

def test_no_duplicates_in_result():
    liked_perfumes = [{"all_notes": ["vanilla", "amber"]}]
    liked_notes = ["amber"]

    result = get_effective_liked_notes(liked_perfumes, liked_notes)

    assert "amber" in result
    assert len(result) == len(set(result))  # no duplicates

def test_returns_empty_when_all_inputs_empty():
    result = get_effective_liked_notes([], [])
    assert result == []