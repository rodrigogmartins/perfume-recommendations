from unittest.mock import patch

from src.perfumes.prioritizer.perfumes_prioritizer import perfumes_prioritizer


@patch("src.perfumes.prioritizer.perfumes_prioritizer.effective_liked_prioritizer")
@patch("src.perfumes.prioritizer.perfumes_prioritizer.day_shift_prioritizer")
@patch("src.perfumes.prioritizer.perfumes_prioritizer.climates_prioritizer")
@patch("src.perfumes.prioritizer.perfumes_prioritizer.seasons_prioritizer")
def test_perfumes_prioritize_score_combination(
    mock_seasons,
    mock_climates,
    mock_day_shift,
    mock_effective_liked
):
    mock_effective_liked.return_value = 10
    mock_day_shift.return_value = 15
    mock_climates.return_value = 18
    mock_seasons.return_value = 25

    perfume = {
        "_id": "p001",
        "all_notes": ["vanilla", "amber"],
        "accords": ["sweet", "woody"],
        "day_shifts": ["day"],
        "climates": ["summer"],
        "seasons": ["spring"],
    }
    user_input = {
        "dayShifts": ["day"],
        "climates": ["summer"],
        "seasons": ["spring"],
        "likedPerfumes": ["p001"],
        "likedNotes": ["amber"],
        "likedAccords": ["sweet"]
    }

    result = perfumes_prioritizer(perfume, user_input)

    assert result == 25
    mock_effective_liked.assert_called_once()
    mock_day_shift.assert_called_once()
    mock_climates.assert_called_once()
    mock_seasons.assert_called_once()

def test_perfume_with_missing_optional_fields(monkeypatch):
    perfume = {
        "_id": "p002",
        "all_notes": [],
        "accords": [],
    }
    result = perfumes_prioritizer(perfume, {})

    assert isinstance(result, int)
