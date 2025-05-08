def climates_prioritizer(score, perfume_climates, climates_user_preferences):
    user_climates = set(climates_user_preferences)

    if user_climates:
        if perfume_climates == user_climates:
            score += 10
        elif user_climates.issubset(perfume_climates):
            score += 5

    return score