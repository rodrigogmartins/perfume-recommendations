def calculate_affinity_score(perfume, user_preferences):
    score = 0.0
    max_score = 0.0

    liked_notes = set(user_preferences["likedNotes"])
    liked_accords = set(user_preferences["likedAccords"])
    perfume_notes = set(perfume.get("all_notes", []))
    perfume_accords = set(perfume.get("accords", []))

    score += len(liked_notes & perfume_notes) * 6.0
    score += len(liked_accords & perfume_accords) * 4.0
    max_score += max(len(liked_notes), 1) * 3.0 + max(len(liked_accords), 1) * 2.0

    not_liked_notes = set(user_preferences["notLikedNotes"])
    not_liked_accords = set(user_preferences["notLikedAccords"])
    score -= len(not_liked_notes & perfume_notes) * 3.0
    score -= len(not_liked_accords & perfume_accords) * 2.0

    prob = max(min(score / max(max_score, 1.0), 1.0), 0.0)

    return round(prob, 2)
