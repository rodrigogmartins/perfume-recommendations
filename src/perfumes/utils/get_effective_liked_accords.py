from collections import Counter

def get_effective_liked_accords(liked_perfumes, liked_accords):
    all_accords = [accord for perfume in liked_perfumes for accord in perfume.get("accords", [])]
    accord_counter = Counter(all_accords)
    inferred_liked_accords = [ac for ac, _ in accord_counter.most_common(3)]

    return list(set(liked_accords + inferred_liked_accords))