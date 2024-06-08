import calculate_digit as cd
import settings as S

def create_sets(generation, dna):
    """
    param: Creates the sets for a given DNA.
    type: int, list[str,...,[int]]
    return: None
    """
    for member in range(S.POPULATION_SIZE):
        with open(S.GEN_FOLDER + str(generation) + '/dna_' + str(member) + '_sets', 'w') as sets_file:
            for i in range(S.SET_SIZE):
                line="" 
                for number in range(S.SET_LENGTH):
                    line += str(cd.calculate_digit(dna)) + ','
                line = line[:-1] + '\n'
                sets_file.write(line)
        sets_file.close()