from random import randint

import settings as S


def calculate_digit(dna):
    """
    param: returns a number from a DNA.
    type: dna: list[str,...[int]]
    return: int
    """
    test_dna = dna.copy()
    key = test_dna[len(test_dna) - 1]
    test_dna.pop()
    for index in key:
        test_dna[index] = str(randint(S.MINIMUM_LETTER_VALUE, S.MAXIMUM_LETTER_VALUE))
    return round(eval(''.join(test_dna)))
