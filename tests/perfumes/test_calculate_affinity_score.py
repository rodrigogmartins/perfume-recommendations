import pytest

from src.perfumes.calculate_affinity_score import calculate_affinity_score


@pytest.fixture
def base_user_preferences():
    return {
        "likedNotes": ["vanilla", "rose"],
        "notLikedNotes": ["oud"],
        "likedAccords": ["sweet", "floral"],
        "notLikedAccords": ["animalic"]
    }

def test_perfect_match(base_user_preferences):
    perfume = {
        "all_notes": ["vanilla", "rose"],
        "accords": ["sweet", "floral"]
    }
    score = calculate_affinity_score(perfume, base_user_preferences)
    assert score == 1.0

def test_partial_match(base_user_preferences):
    perfume = {
        "all_notes": ["vanilla", "oud"],
        "accords": ["sweet", "woody"]
    }
    score = calculate_affinity_score(perfume, base_user_preferences)
    assert 0.0 < score < 1.0

def test_no_match(base_user_preferences):
    perfume = {
        "all_notes": ["oud"],
        "accords": ["animalic"]
    }
    score = calculate_affinity_score(perfume, base_user_preferences)
    assert score == 0.0

def test_empty_perfume_data(base_user_preferences):
    perfume = {
        "all_notes": [],
        "accords": []
    }
    score = calculate_affinity_score(perfume, base_user_preferences)
    assert score == 0.0

def test_empty_user_preferences():
    user_preferences = {
        "likedNotes": [],
        "notLikedNotes": [],
        "likedAccords": [],
        "notLikedAccords": []
    }
    perfume = {
        "all_notes": ["vanilla"],
        "accords": ["sweet"]
    }
    score = calculate_affinity_score(perfume, user_preferences)
    assert score == 0.0
