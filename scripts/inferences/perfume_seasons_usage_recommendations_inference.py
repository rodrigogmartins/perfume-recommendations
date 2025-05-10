def get_seasons_recommendations_inference(acordes_param):
    seasons = set()

    if any(a in acordes_param for a in ["floral", "fruity", "ozonic", "green", "herbal", "white floral", "powdery", "aromatic"]):
        seasons.add("spring")
    if any(a in acordes_param for a in ["citrus", "aquatic", "ozonic", "green", "herbal", "fresh", "fresh spicy", "tropical", "white floral"]):
        seasons.add("summer")
    if any(a in acordes_param for a in ["spicy", "woody", "leather", "musky", "earthy", "aromatic", "smoky"]):
        seasons.add("fall")
    if any(a in acordes_param for a in ["amber", "sweet", "gourmand", "resinous", "balsamic", "leather", "musky", "smoky", "incense", "animalic"]):
        seasons.add("winter")
    if not seasons:
        seasons.update(["spring", "summer", "fall", "winter"])

    return list(seasons)