def day_shift_prioritizer(score, perfume_day_shifts, day_shifts_user_preferences):
    user_day_shifts = set(day_shifts_user_preferences)

    if user_day_shifts:
        if perfume_day_shifts == user_day_shifts:
            score += 10
        elif user_day_shifts.issubset(perfume_day_shifts):
            score += 5

    return score