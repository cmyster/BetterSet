from random import randint, getrandbits
import is_valid
import settings as S


def get_dna(member):
    """
    param: returns a valid dna.
    type: int
    return: list[str,...,[int]]
    """
    while True:
        dna = []
        key = []
        dna_length = randint(S.DNA_MIN_LENGTH, S.DNA_MAX_LENGTH)
        for letter in range(dna_length):
            if letter % 2 == 0:
                if randint(1, 100) <= S.RANDOM_CHANCE:
                    key.append(letter)  # The letter at this index would later be randomly generated.
            digit = randint(S.MINIMUM_LETTER_VALUE, S.MAXIMUM_LETTER_VALUE)
            dna.append(str(digit))  # Saving as a string S. we can use eval later.
            operator = S.OPERATORS[getrandbits(2)]
            dna.append(operator)
        # Last element is an operator and we want to remove it now.
        dna.pop()
        dna.append(key)
        if is_valid(dna):
            print("Generated DNA: " + str(member + 1) + " out of: " + str(S.POPULATION_SIZE))
            return dna
