def effective_liked_prioritizer(
    score,
    perfume_id,
    liked_perfume_ids,
    perfume_notes,
    effective_liked_notes,
    perfume_accords,
    effective_liked_accords,
):

    score += len(set(perfume_notes) & set(effective_liked_notes)) * 2
    score += len(set(perfume_accords) & set(effective_liked_accords)) * 3
    score += 5 if perfume_id in liked_perfume_ids else 0

    return score