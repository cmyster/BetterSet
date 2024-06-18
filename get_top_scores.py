import settings as S


def get_top_scores(scores):
    """
    param: Returns a list of indices of the top DNAs in a generation.
    type: list[int]
    return: list[int]
    """
    # We need to keep the top score and its index.
    temp_scores = scores.copy()
    top_scores = []
    for top_score in range(S.POPULATION_SIZE - 1):
        top_scores.append(temp_scores.index(max(temp_scores)))
        temp_scores[temp_scores.index(max(temp_scores))] = 0
    return top_scores
