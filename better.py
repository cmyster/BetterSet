#!/usr/bin/python

"""
This script uses randomly created "DNA" sequences to generate sets of numbers.
The sets will be measured against a test file and its success rate will be calculated
as how close the generated sets were against the ones in the test file.
Every generation, the most successful DNAs will be used, some merged, some mutated,
to create the next generation.

The end goal of the game is to create an instruction set  that will generate sets
of numbers in predictable way. If your test files contains random numbers, then the
instructions will eventually, given enough time, create random numbers as well in
the given range.

Example of a test file (you can use generate_test.py):
1,2,3,4,5,6,7,8,9,10
2,3,4,5,6,7,8,9,10,11
3,4,5,6,7,8,9,10,11,12
...

Example of a DNA:
Pairs of numbers and operators, the last element is a list of indices that will be randomly
generated.
['5', '-', '2', '*', '2', '-', '3', '/', '2', [0, 2]]

TODO:
1. Instead of picking the top performing DNAs, use logarithmic distribution to have of
better-performing DNAs and less of the less-performing ones.
2. Functions wants to live in their own files.
3. Calculations are linear:
    a. Some functions can be delegated to different threads. This needs a waiter function.
    b. Some calculations should be vectorized.
"""

from math import log
from numpy import mean
from random import getrandbits, randint, randrange
from shutil import rmtree
from os import mkdir, path

"""
DNA_MIN/MAX_LENGTH is the length of the DNA. The longer it is, the more complex
the DNA is and the longer it takes to be generated; but it will give you a better
mix of numbers. The shorter it is, the less complex the DNA, and generated sets will
be very similar to one another, and it will take less time to run.
"""
DNA_MIN_LENGTH = 50          # Minimum length of a DNA.
DNA_MAX_LENGTH = 100         # Maximum length of a DNA.

MINIMUM_DIGIT = 1            # Minimum digit that can be generated.
MAXIMUM_DIGIT = 50           # Maximum digit that can be generated.
POPULATION_SIZE = 100        # How many DNA are there in a generation.
GENERATIONS = 100            # How many generations are there in a simulation.
SET_LENGTH = 10              # How many digits in a set.

"""
SET_SIZE means how many lines of sets are there for a given DNA. This is also how many times the DNA
is tested to see if it can generate a number between MINIMUM_DIGIT and MAXIMUM_DIGIT. If it can, then
it is considered healthy.
Too small a size will not give good results, and too large a size will take a very long time to generate.
"""
SET_SIZE = 1000              # How many sets each DNA generates. Also how many tests each DNA has to pass.

OPERATORS = [
    '+', '-', '*', '/']      # 4 operators only, so we can use getrandbits(2) which is faster.

RANDOM_CHANCE = 15           # % out of 100 would be random letter in the "DNA" and the rest are constant.
MINIMUM_LETTER_VALUE = 1     # Minimum value of a letter.
MAXIMUM_LETTER_VALUE = 7     # Maximum value of a letter.

# HEALTH checks:
"""
SET_HEALTH needs to be smaller than or equal to SET_SIZE and larger than 0. This will indicate how
healthy a DNA might be, as the relative number of healthy runs out of all runs. As an example, if a
single DNA generates 100 sets, and the health is set to 90, then we will test that the DNA can create
a number between MINIMUM_DIGIT and MAXIMUM_DIGIT for 100 times and if it created digits in the range
for more than 90 times, it is considered a healthy DNA.

The closer SET_HEALTH is to SET_SIZE, the longer it takes to generate a healthy DNA.
If SET_HEALTH == SET_SIZE, it will take a long time to generate, but also you might miss out:
Consider that we generated a DNA that constantly guesses correctly 4 out of 5 numbers. That's pretty good!
But that 1 out of 5 is a number outside the range, so we deleted that DNA... A small amount of errors is not
always bad.
"""
SET_HEALTH = 970
GEN_FOLDER = "generation-"   # The folder name for each generation.
TEST_FILE = "./test.csv"     # The file that contains the test sets.
if not path.exists(TEST_FILE):
    print("Test file not found.")
    exit(1)

"""
Parameters for generational changes:
"""
ASCENDING = 60               # Percentage of top DNAs that are taken from the previous generation.
DNA_MUTATION_RATE = 1        # Percentage of the DNA that is mutated.
DNA_MIX_RATE = 10            # Percentage of the DNAs that mix together (sort of sexual reproduction).

"""
CROSS_OVER is the process of taking a letter + operator pair (values are doubled in the function later)
from a random DNA that was also in the generation top DNAs, and replacing it at a random spot.
"""
CROSSOVER_MIN_LENGTH = 1     # Minimum length of the DNA that is crossed-over.
CROSSOVER_MAX_LENGTH = 3     # Maximum length of the DNA that is crossed-over.

def calculate_digit(dna):
    """
    param: returns a number from a DNA.
    type: dna: list[str,...[int]]
    return: int
    """
    test_dna = dna.copy()
    key=test_dna[len(test_dna) - 1]
    test_dna.pop()
    for index in key:
        test_dna[index] = str(randint(MINIMUM_LETTER_VALUE, MAXIMUM_LETTER_VALUE))
    return round(eval(''.join(test_dna)))

def valid(dna):
    """
    param: returns a bool for DNA health.
    type: dna: list[str,...,[int]]
    return: bool
    """
    test_dna = dna.copy()
    key = test_dna[len(test_dna)-1]
    results = [0] * (MAXIMUM_DIGIT + 1) # Part of the health-check is to see how many repetitions we got.
    health = 0
    for item in range(SET_SIZE):
        if len(key)-1 > 0:
            result = calculate_digit(test_dna)
        else:
            return False
        if result >= MINIMUM_DIGIT and result <= MAXIMUM_DIGIT:
            health += 1
            results[result] += 1
    for index in range(len(results) - 1):
        if results[index] > 1:
            health -= 1
    if health >= SET_HEALTH:
        return True

def get_dna():
    """
    param: returns a valid dna.
    type: None
    return: list[str,...,[int]]
    """
    while True:
        dna = []
        key = []
        dna_length = randint(DNA_MIN_LENGTH, DNA_MAX_LENGTH)
        for letter in range(dna_length):
            if letter % 2 == 0:
                if randint(1, 100) <= RANDOM_CHANCE:
                    key.append(letter) # The letter at this index would later be randomly generated.
            digit = randint(MINIMUM_LETTER_VALUE, MAXIMUM_LETTER_VALUE)
            dna.append(str(digit)) # Saving as a string so we can use eval later.
            operator = OPERATORS[getrandbits(2)]
            dna.append(operator)
        dna.pop()
        dna.append(key)
        if valid(dna):
            return dna

def create_folder(name, index):
    """
    param: Generates a folder based on name and index number.
    type: str, int
    return: str
    """
    folder = name + str(index)
    if path.exists(folder):
        rmtree(folder)
    mkdir(folder)
    return folder

def assess(sum_set):
    """
    param: Assesses the set against the sets in the test file.
    type: set(list)
    return: int
    """
    score = 0
    with open(TEST_FILE, 'r') as test_file:
        for test_set in test_file:
            for digit in sum_set:
                if digit in test_set:
                    score += 1
    test_file.close()
    # Adding a bias here so that the score will be lower if the set had low uniqueness.
    score = score * log(len(sum_set) + 1 ,SET_LENGTH)
    return int(score)

def get_top_scores(scores):
    """
    param: Returns a list of indices of the top DNAs in a generation.
    type: list[int]
    return: list[int]
    """
    # We need to keep the top score and its index.
    temp_scores = scores.copy()
    top_scores = []
    for top_score in range(int((POPULATION_SIZE * ASCENDING) // 100)):
        top_scores.append(temp_scores.index(max(temp_scores)))
        temp_scores[temp_scores.index(max(temp_scores))] = 0
    return top_scores

def mutate_dna(temp_dna):
    """
    param: Mutates the DNA.
    type: list[str,...,[int]]
    return: None
    """
    index_to_change = randrange(0, len(temp_dna) - 1, 2)
    current_value = temp_dna[index_to_change]
    while True:
        new_value = str(randint(MINIMUM_LETTER_VALUE, MAXIMUM_LETTER_VALUE))
        if new_value != current_value:
            temp_dna[index_to_change] = new_value
            break

def mix_dna(temp_dna, index_to_mix, generation):
    """
    param: Mixes the DNA with another DNA.
    type: list[str,...,[int]], int, int
    return: None
    """
    with open(GEN_FOLDER + str(generation) + '/dna_' + str(index_to_mix), 'r') as dna_file:
        donor_dna = list(dna_file.read().split(','))
        dna_file.close()
    # How many letters and operators we are going to mix.
    cross_length = randint(CROSSOVER_MIN_LENGTH, CROSSOVER_MAX_LENGTH) * 2
    start_index_receiver = randrange(0, (len(temp_dna) - 1) - cross_length, 2)
    start_index_donor = randrange(0, (len(donor_dna) - 1) - cross_length, 2)
    for index in range(cross_length - 1):
        temp_dna[start_index_receiver + index] = donor_dna[start_index_donor + index]


def ascend_dna(generation_top_scores, generation):
    """
    param: Ascends the DNA to the next generation.
    type: list[[int, int]], int
    return: None
    """
    loop_index = 0
    for current_gen_index in generation_top_scores:
        with open(GEN_FOLDER + str(generation) + '/dna_' + str(current_gen_index), 'r') as dna_file:
            tmp_dna = list(dna_file.read().split(','))
        dna_file.close()
        if randint(1, 100) <= DNA_MUTATION_RATE:
            mutate_dna(tmp_dna)
        if randint(1, 100) <= DNA_MIX_RATE:
            while True:
                index_to_mix = generation_top_scores[randint(0, len(generation_top_scores) - 1)]
                if index_to_mix != current_gen_index:
                    break
            mix_dna(tmp_dna, index_to_mix, generation)
        with open(GEN_FOLDER + str(generation + 1) + '/dna_' + str(loop_index), 'w') as dna_file:
            dna_file.write(str(tmp_dna))
        dna_file.close()
        loop_index += 1

def complete_next_generation(generation, top_scores_length):
    """
    param: Completes the next generation with random DNAs.
    type: int, int
    return: None
    """
    for index_to_complete in range(POPULATION_SIZE - top_scores_length, POPULATION_SIZE - 1):
        with open(GEN_FOLDER + str(generation + 1) + '/dna_' + str(index_to_complete), 'w') as dna_file:
            dna_file.write(str(get_dna()))
            dna_file.close()
    for member in range(POPULATION_SIZE):
        if not path.exists(GEN_FOLDER + str(generation) + '/dna_' + str(member)):
            with open(GEN_FOLDER + str(generation + 1) + '/dna_' + str(member), 'w') as dna_file:
                dna_file.write(str(get_dna()))
                dna_file.close()            

def main():
    """
    param: Main function, creates "healthy" DNAs for gen-0 and their files. gen-1+ will be generated from gen-0.
    Calculating stuff happens elsewhere.
    type: None
    return: None
    """
    # Create the first generation.
    gen_folder = create_folder(GEN_FOLDER, 0)
    for member in range(POPULATION_SIZE):
        dna = get_dna()
        with open(gen_folder + '/dna_' + str(member), 'w') as dna_file:
            dna_file.write(str(dna))
            dna_file.close()
    # Assess each generation, get the healthiest DNAs and create the next generation.
    for generation in range(GENERATIONS):
        # Create the sets for each DNA.
        for member in range(POPULATION_SIZE):
            with open(GEN_FOLDER + str(generation) + '/dna_' + str(member) + '_sets', 'w') as sets_file:
                for i in range(SET_SIZE):
                    line="" 
                    for number in range(SET_LENGTH):
                        line += str(calculate_digit(dna)) + ','
                    line = line[:-1] + '\n'
                    sets_file.write(line)
            sets_file.close()
        # Assess the sets and get the top scores.
        generation_top_scores = []
        current_gen_folder = gen_folder # This we learned from fibonacci()
        next_gen_folder = create_folder(GEN_FOLDER, generation + 1)
        gen_folder = next_gen_folder
        dna_scores = []
        for current_sets_file in range(POPULATION_SIZE - 1):
            with open (current_gen_folder + '/dna_' + str(current_sets_file) + '_sets', 'r') as sets_file:
                set_scores = []
                for set_line in sets_file:
                    set_scores.append(assess(list(set(set_line.split(',')))))
            sets_file.close()
            dna_scores.append(int(mean(set_scores)))
        generation_top_scores = get_top_scores(dna_scores)
        with open (current_gen_folder + '/top_scores', 'w') as top_scores_file:
            for score in generation_top_scores:
                top_scores_file.write(str(score) + '\n')
        top_scores_file.close()
        ascend_dna(generation_top_scores, generation)
        complete_next_generation(generation, len(generation_top_scores))

if __name__ == '__main__':
    main()