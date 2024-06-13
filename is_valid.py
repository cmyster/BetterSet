import settings as S
from calculate_digit import calculate_digit as cd


def is_valid(dna):
    """
    param: returns a bool for DNA health.
    type: dna: list[str,...,[int]]
    return: bool
    """
    test_dna = dna.copy()
    key = test_dna[len(test_dna)-1]
    results = [0] * (S.MAXIMUM_DIGIT + 1)  # Part of the health-check is to see how many repetitions we got.
    health = 0
    for item in range(S.SET_SIZE):
        if len(key)-1 > 0:
            result = cd(test_dna)
        else:
            return False
        if result >= S.MINIMUM_DIGIT and result <= S.MAXIMUM_DIGIT:
            health += 1
            results[result] += 1
    if sum(results) > S.SET_HEALTH:
        for index in range(len(results) - 1):
            if results[index] > 1:
                health -= 1
    if health >= S.SET_HEALTH:
        return True
    return False
