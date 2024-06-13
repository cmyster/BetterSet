from ast import literal_eval
from random import randint, randrange

import settings as S


def mix_dna(temp_dna, index_to_mix, generation):
    """
    param: Mixes the DNA with another DNA.
    type: list[str,...,[int]], int, int
    return: None
    """
    with open(S.GEN_FOLDER + str(generation) + '/dna_' + str(index_to_mix), 'r') as dna_file:
        donor_dna = literal_eval(dna_file.read())
        dna_file.close()
    # How many letters and operators we are going to mix.
    cross_length = randint(S.CHANGE_MIN_LENGTH, S.CHANGE_MAX_LENGTH) * 2
    start_index_receiver = randrange(0, (len(temp_dna) - 1) - cross_length, 2)
    start_index_donor = randrange(0, (len(donor_dna) - 1) - cross_length, 2)
    for index in range(cross_length - 1):
        temp_dna[start_index_receiver + index] = donor_dna[start_index_donor + index]
