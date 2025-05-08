from src.perfumes.prioritizer.rules.day_shift_prioritizer import day_shift_prioritizer


def test_exact_match_adds_10():
    score = 70
    perfume_day_shifts = {"day", "night"}
    user_prefs = {"day", "night"}
    result = day_shift_prioritizer(score, perfume_day_shifts, user_prefs)
    assert result == 80

def test_subset_match_adds_5():
    score = 60
    perfume_day_shifts = {"day", "night", "evening"}
    user_prefs = {"day", "night"}
    result = day_shift_prioritizer(score, perfume_day_shifts, user_prefs)
    assert result == 65

def test_no_overlap_adds_0():
    score = 50
    perfume_day_shifts = {"evening"}
    user_prefs = {"day", "night"}
    result = day_shift_prioritizer(score, perfume_day_shifts, user_prefs)
    assert result == 50

def test_user_preferences_empty_adds_0():
    score = 40
    perfume_day_shifts = {"day"}
    user_prefs = []
    result = day_shift_prioritizer(score, perfume_day_shifts, user_prefs)
    assert result == 40

def test_perfume_day_shifts_exact_order_does_not_matter():
    score = 30
    perfume_day_shifts = {"night", "day"}
    user_prefs = ["day", "night"]
    result = day_shift_prioritizer(score, perfume_day_shifts, user_prefs)
    assert result == 40