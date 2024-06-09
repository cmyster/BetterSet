from random import randint
from ast import literal_eval
from mix_dna import mix_dna
from mutate_dna import mutate_dna
import settings as S

def ascend_dna(generation_top_scores, generation):
    """
    param: Ascends the DNA to the next generation.
    type: list[[int, int]], int
    return: None
    """
    loop_index = 0
    for current_gen_index in generation_top_scores:
        with open(S.GEN_FOLDER + str(generation) + '/dna_' + str(current_gen_index), 'r') as dna_file:
            tmp_dna = literal_eval(dna_file.read())
        dna_file.close()
        if randint(1, 100) <= S.DNA_MUTATION_RATE:
            mutate_dna(tmp_dna)
        if randint(1, 100) <= S.DNA_MIX_RATE:
            while True:
                index_to_mix = generation_top_scores[randint(0, len(generation_top_scores) - 1)]
                if index_to_mix != current_gen_index:
                    break
            mix_dna(tmp_dna, index_to_mix, generation)
        with open(S.GEN_FOLDER + str(generation + 1) + '/dna_' + str(loop_index), 'w') as dna_file:
            dna_file.write(str(tmp_dna))
        dna_file.close()
        loop_index += 1