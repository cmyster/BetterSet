from random import randrange

import settings as S


def reducnnt_pairs(temp_dna):
    """
    param: Takes a DNA and duplicates pairs in a random location.
    type: list[str,...,[int]]
    return: list[str,...,[int]]
    """
    index_of_change = randrange(0, len(temp_dna) - 1, 2)
    pairs_to_reduct = randrange(S.CHANGE_MIN_LENGTH, S.CHANGE_MAX_LENGTH)
    for pair in range(pairs_to_reduct):
        temp_dna.pop(index_of_change)
    return temp_dna
