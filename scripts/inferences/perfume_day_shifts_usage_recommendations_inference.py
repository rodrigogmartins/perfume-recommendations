def get_day_shifts_recommendations_inference(accords):
    day_shifts = set()

    if any(a in accords for a in [
        "amber", "gourmand", "musky", "sweet", "leather", "woody", "resinous",
        "balsamic", "smoky", "animalic", "incense", "spicy", "oriental"
    ]):
        day_shifts.add("night")

    if any(a in accords for a in [
        "citrus", "aquatic", "green", "fresh", "ozonic", "floral", "white floral",
        "herbal", "fruity", "aromatic", "powdery", "fresh spicy", "tropical"
    ]):
        day_shifts.add("day")

    if not day_shifts:
        day_shifts.update(["day", "night"])

    return list(day_shifts)
