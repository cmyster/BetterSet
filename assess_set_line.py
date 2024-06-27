from math import log

import settings as S


def assess_set_line(sum_set):
    """
    param: Assesses a set against the sets in the test file.
    type: set(list)
    return: int
    """
    score = 0
    with open(S.TEST_FILE, 'r') as test_file:
        
        for test_set in test_file:
            for digit in sum_set:
                if int(digit) >= S.MINIMUM_DIGIT and int(digit) <= S.MAXIMUM_DIGIT:
                    if digit in test_set:
                        score += 1
    test_file.close()
    # Adding a bias here that the score will be lower if the set had low uniqueness.
    score = score * log(len(sum_set) + 1, S.SET_LENGTH)
    return int(score)
