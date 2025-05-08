from src.perfumes.prioritizer.rules.effective_liked_prioritizer import effective_liked_prioritizer


def test_all_factors_contribute():
    score = 10
    perfume_id = "p123"
    liked_perfume_ids = {"p123", "p456"}
    perfume_notes = {"vanilla", "amber", "jasmine"}
    effective_liked_notes = {"amber", "jasmine", "rose"}
    perfume_accords = {"woody", "sweet"}
    effective_liked_accords = {"sweet", "fresh"}

    # 2 notas em comum * 2 = 4
    # 1 acorde em comum * 3 = 3
    # perfume_id in liked_perfume_ids => +5
    expected = 10 + 4 + 3 + 5
    result = effective_liked_prioritizer(
        score,
        perfume_id,
        liked_perfume_ids,
        perfume_notes,
        effective_liked_notes,
        perfume_accords,
        effective_liked_accords
    )
    assert result == expected

def test_no_matches_adds_nothing():
    score = 0
    perfume_id = "p000"
    liked_perfume_ids = {"p123", "p456"}
    perfume_notes = {"vanilla"}
    effective_liked_notes = {"rose"}
    perfume_accords = {"woody"}
    effective_liked_accords = {"fresh"}

    result = effective_liked_prioritizer(
        score,
        perfume_id,
        liked_perfume_ids,
        perfume_notes,
        effective_liked_notes,
        perfume_accords,
        effective_liked_accords
    )
    assert result == 0

def test_only_liked_perfume_adds_5():
    score = 1
    perfume_id = "p123"
    liked_perfume_ids = {"p123"}
    result = effective_liked_prioritizer(
        score,
        perfume_id,
        liked_perfume_ids,
        [],
        [],
        [],
        []
    )
    assert result == 6

def test_only_notes_match():
    score = 5
    perfume_id = "x"
    liked_perfume_ids = {"other"}
    perfume_notes = {"jasmine", "amber"}
    effective_liked_notes = {"amber", "vanilla"}
    result = effective_liked_prioritizer(
        score,
        perfume_id,
        liked_perfume_ids,
        perfume_notes,
        effective_liked_notes,
        [],
        []
    )
    # 1 note match => 2 points
    assert result == 7

def test_only_accords_match():
    score = 2
    perfume_id = "y"
    liked_perfume_ids = {}
    perfume_accords = {"fresh", "powdery"}
    effective_liked_accords = {"powdery", "green"}
    result = effective_liked_prioritizer(
        score,
        perfume_id,
        liked_perfume_ids,
        [],
        [],
        perfume_accords,
        effective_liked_accords
    )
    # 1 accord match => 3 points
    assert result == 5