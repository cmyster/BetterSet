from ast import literal_eval

from calculate_digit import calculate_digit as cd
import settings as S


def create_sets(GENERATION, member):
    """
    param: Creates the sets for a given DNA.
    type: int, int
    return: None
    """
    print("Creating sets for member: " + str(member + 1))
    with open(S.GEN_FOLDER + str(GENERATION) + '/dna_' + str(member), "r") as dna_file:
        dna = literal_eval(dna_file.read())
        dna_file.close()
    with open(S.GEN_FOLDER + str(GENERATION) + '/dna_' + str(member) + '_sets', 'w') as sets_file:
        for i in range(S.SET_SIZE):
            line = ""
            for number in range(S.SET_LENGTH):
                line += str(cd(dna)) + ','
            line = line[:-1] + '\n'
            sets_file.write(line)
    sets_file.close()
