from random import randint, randrange
import settings as S

def mutate_dna(temp_dna):
    """
    param: Mutates the DNA.
    type: list[str,...,[int]]
    return: None
    """
    index_to_change = randrange(0, len(temp_dna) - 1, 2)
    current_value = temp_dna[index_to_change]
    while True:
        new_value = str(randint(S.MINIMUM_LETTER_VALUE, S.MAXIMUM_LETTER_VALUE))
        if new_value != current_value:
            temp_dna[index_to_change] = new_value
            break