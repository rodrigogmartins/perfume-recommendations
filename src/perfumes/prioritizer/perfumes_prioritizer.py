from src.perfumes.prioritizer.rules.effective_liked_prioritizer import effective_liked_prioritizer
from src.perfumes.prioritizer.rules.day_shift_prioritizer import day_shift_prioritizer
from src.perfumes.prioritizer.rules.climates_prioritizer import climates_prioritizer
from src.perfumes.prioritizer.rules.seasons_prioritizer import seasons_prioritizer

def perfumes_prioritizer(
    perfume,
    user_input_query=None
):

    score = 0
    perfume_notes = perfume.get("all_notes", [])
    perfume_accords = perfume.get("accords", [])
    perfume_day_shifts = set(perfume.get("day_shifts", []))
    perfume_climates = set(perfume.get("climates", []))
    perfume_seasons = set(perfume.get("seasons", []))
    liked_perfume_ids = set(user_input_query.get("likedPerfumes", []))
    liked_perfume_notes = set(user_input_query.get("likedNotes", []))
    liked_perfume_accords = set(user_input_query.get("likedAccords", []))

    score = effective_liked_prioritizer(
        score,
        perfume["_id"],
        liked_perfume_ids,
        perfume_notes,
        liked_perfume_notes,
        perfume_accords,
        liked_perfume_accords
    )
    score = day_shift_prioritizer(score, perfume_day_shifts, user_input_query.get("dayShifts", []))
    score = climates_prioritizer(score, perfume_climates, user_input_query.get("climates", []))
    score = seasons_prioritizer(score, perfume_seasons, user_input_query.get("seasons", []))

    return score