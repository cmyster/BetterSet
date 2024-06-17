from get_dna import get_dna


def generate_member(member, gen_folder):
    dna = get_dna(member)
    with open(gen_folder + '/dna_' + str(member), 'w') as dna_file:
        dna_file.write(str(dna))
        dna_file.close()
