import settings as S


def get_top_scores(current_gen_folder):
    """
    param: Returns a list of indices of the top DNAs in a generation.
    type: str
    return: list[int]
    """
    # We need to keep the top score and its index.
    temp_top_scores = []
    for member in range(S.POPULATION_SIZE):
        with open(current_gen_folder + '/dna_' + str(member) + '_mean', 'r') as mean_file:
            mean = mean_file.read()
            mean_file.close()
        temp_top_scores.append(int(mean))
    top_scores = []
    for top_score in range(S.POPULATION_SIZE):
        top_scores.append(temp_top_scores.index(max(temp_top_scores)))
        temp_top_scores[temp_top_scores.index(max(temp_top_scores))] = 0
    return top_scores
