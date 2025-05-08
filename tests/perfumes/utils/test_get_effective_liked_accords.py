from src.perfumes.utils.get_effective_liked_accords import get_effective_liked_accords

def test_merges_liked_and_inferred_accords():
    liked_perfumes = [
        {"accords": ["woody", "citrus", "spicy"]},
        {"accords": ["woody", "spicy", "sweet"]},
        {"accords": ["woody", "amber", "spicy"]},
    ]
    liked_accords = ["floral"]

    result = get_effective_liked_accords(liked_perfumes, liked_accords)

    # "woody" and "spicy" are most common (3 times), "citrus" and others less
    assert set(result) == set(["floral", "woody", "spicy", "sweet"]) or set(result) == set(["floral", "woody", "spicy", "amber"]) or set(result) == set(["floral", "woody", "spicy", "citrus"])

def test_returns_only_liked_accords_when_perfumes_empty():
    liked_perfumes = []
    liked_accords = ["green", "fruity"]

    result = get_effective_liked_accords(liked_perfumes, liked_accords)

    assert set(result) == set(["green", "fruity"])

def test_no_duplicates_in_final_result():
    liked_perfumes = [{"accords": ["amber", "vanilla"]}]
    liked_accords = ["amber"]

    result = get_effective_liked_accords(liked_perfumes, liked_accords)

    assert result.count("amber") == 1
    assert len(result) == len(set(result))

def test_returns_empty_when_both_inputs_empty():
    result = get_effective_liked_accords([], [])
    assert result == []
