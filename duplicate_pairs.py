from random import randrange

import settings as S


def duplicate_pairs(temp_dna):
    """
    param: Takes a DNA and duplicates pairs in a random location.
    type: list[str,...,[int]]
    return: list[str,...,[int]]
    """
    index_of_change = randrange(0, len(temp_dna) - 1, 2)
    pairs_to_change = randrange(S.CHANGE_MIN_LENGTH, S.CHANGE_MAX_LENGTH)
    for pair in range(pairs_to_change):
        current_value = temp_dna[index_of_change]
    temp_dna.insert(index_of_change, current_value)
    return temp_dna
