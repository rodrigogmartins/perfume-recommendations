from src.perfumes.prioritizer.rules.climates_prioritizer import climates_prioritizer

def test_exact_match_adds_10():
    score = 50
    perfume_climates = {"summer", "spring"}
    user_prefs = {"summer", "spring"}
    result = climates_prioritizer(score, perfume_climates, user_prefs)
    assert result == 60

def test_subset_match_adds_5():
    score = 40
    perfume_climates = {"summer", "spring", "fall"}
    user_prefs = {"summer", "spring"}
    result = climates_prioritizer(score, perfume_climates, user_prefs)
    assert result == 45

def test_no_overlap_adds_0():
    score = 30
    perfume_climates = {"winter"}
    user_prefs = {"summer", "spring"}
    result = climates_prioritizer(score, perfume_climates, user_prefs)
    assert result == 30

def test_user_preferences_empty_adds_0():
    score = 20
    perfume_climates = {"summer"}
    user_prefs = []
    result = climates_prioritizer(score, perfume_climates, user_prefs)
    assert result == 20

def test_perfume_climates_exact_order_does_not_matter():
    score = 10
    perfume_climates = {"spring", "summer"}
    user_prefs = ["summer", "spring"]
    result = climates_prioritizer(score, perfume_climates, user_prefs)
    assert result == 20