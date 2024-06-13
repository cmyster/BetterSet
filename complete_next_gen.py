from os import path

from get_dna import get_dna
import settings as S


def complete_next_gen(generation, top_scores_length):
    """
    param: Completes the population with random DNAs.
    type: int, int
    return: None
    """
    for index_to_complete in range(top_scores_length, S.POPULATION_SIZE):
        with open(S.GEN_FOLDER + str(generation + 1) + '/dna_' + str(index_to_complete), 'w') as dna_file:
            dna_file.write(str(get_dna(index_to_complete)))
            dna_file.close()
    for member in range(S.POPULATION_SIZE):
        if not path.exists(S.GEN_FOLDER + str(generation) + '/dna_' + str(member)):
            with open(S.GEN_FOLDER + str(generation + 1) + '/dna_' + str(member), 'w') as dna_file:
                dna_file.write(str(get_dna(generation)))
                dna_file.close()
