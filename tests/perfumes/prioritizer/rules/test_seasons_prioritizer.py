from src.perfumes.prioritizer.rules.seasons_prioritizer import seasons_prioritizer

def test_exact_match_adds_10():
    score = 25
    perfume_seasons = {"summer", "spring"}
    user_prefs = {"spring", "summer"}
    result = seasons_prioritizer(score, perfume_seasons, user_prefs)
    assert result == 35

def test_subset_match_adds_5():
    score = 15
    perfume_seasons = {"summer", "spring", "fall"}
    user_prefs = {"spring"}
    result = seasons_prioritizer(score, perfume_seasons, user_prefs)
    assert result == 20

def test_no_overlap_adds_0():
    score = 10
    perfume_seasons = {"winter"}
    user_prefs = {"spring", "summer"}
    result = seasons_prioritizer(score, perfume_seasons, user_prefs)
    assert result == 10

def test_user_preferences_empty_adds_0():
    score = 5
    perfume_seasons = {"spring"}
    user_prefs = []
    result = seasons_prioritizer(score, perfume_seasons, user_prefs)
    assert result == 5

def test_perfume_seasons_exact_order_does_not_matter():
    score = 0
    perfume_seasons = {"fall", "spring"}
    user_prefs = ["spring", "fall"]
    result = seasons_prioritizer(score, perfume_seasons, user_prefs)
    assert result == 10