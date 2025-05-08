def get_climates_recommendations_inference(accords):
    climates = set()

    if any(a in accords for a in [
        "amber", "gourmand", "leather", "woody", "resinous", "balsamic",
        "musky", "smoky", "incense"
    ]):
        climates.add("cold")

    if any(a in accords for a in [
        "citrus", "aquatic", "ozonic", "green", "fresh", "herbal",
        "fruity", "white floral", "powdery", "fresh spicy"
    ]):
        climates.add("hot")

    if not climates:
        climates.add("mild")

    return list(climates)
