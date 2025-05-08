def seasons_prioritizer(score, perfume_seasons, seasons_user_preferences):
    user_seasons = set(seasons_user_preferences)

    if user_seasons:
        if perfume_seasons == user_seasons:
            score += 10
        elif user_seasons.issubset(perfume_seasons):
            score += 5

    return score