from collections import Counter

def get_effective_liked_notes(liked_perfumes, liked_notes):
    all_notes = [note for perfume in liked_perfumes for note in perfume.get("all_notes", [])]
    note_counter = Counter(all_notes)
    inferred_liked_notes = [note for note, _ in note_counter.most_common(3)]

    return list(set(liked_notes + inferred_liked_notes))