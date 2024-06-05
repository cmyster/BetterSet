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

import settings as s

from math import log
from numpy import mean
from random import getrandbits, randint, randrange
from shutil import rmtree
from os import mkdir, path

if not path.exists(s.TEST_FILE):
    print("Test file not found.")
    exit(1)


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
        test_dna[index] = str(randint(s.MINIMUM_LETTER_VALUE, s.MAXIMUM_LETTER_VALUE))
    return round(eval(''.join(test_dna)))

def valid(dna):
    """
    param: returns a bool for DNA health.
    type: dna: list[str,...,[int]]
    return: bool
    """
    test_dna = dna.copy()
    key = test_dna[len(test_dna)-1]
    results = [0] * (s.MAXIMUM_DIGIT + 1) # Part of the health-check is to see how many repetitions we got.
    health = 0
    for item in range(s.SET_SIZE):
        if len(key)-1 > 0:
            result = calculate_digit(test_dna)
        else:
            return False
        if result >= s.MINIMUM_DIGIT and result <= s.MAXIMUM_DIGIT:
            health += 1
            results[result] += 1
    if sum(results) > s.SET_HEALTH:
        for index in range(len(results) - 1):
            if results[index] > 1:
                health -= 1
    if health >= s.SET_HEALTH:
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
        dna_length = randint(s.DNA_MIN_LENGTH, s.DNA_MAX_LENGTH)
        for letter in range(dna_length):
            if letter % 2 == 0:
                if randint(1, 100) <= s.RANDOM_CHANCE:
                    key.append(letter) # The letter at this index would later be randomly generated.
            digit = randint(s.MINIMUM_LETTER_VALUE, s.MAXIMUM_LETTER_VALUE)
            dna.append(str(digit)) # Saving as a string so we can use eval later.
            operator = s.OPERATORS[getrandbits(2)]
            dna.append(operator)
        # Last element is an operator and we want to remove it now.
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
    with open(s.TEST_FILE, 'r') as test_file:
        for test_set in test_file:
            for digit in sum_set:
                if digit in test_set:
                    score += 1
    test_file.close()
    # Adding a bias here so that the score will be lower if the set had low uniqueness.
    score = score * log(len(sum_set) + 1 ,s.SET_LENGTH)
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
    for top_score in range(int((s.POPULATION_SIZE * s.ASCENDING) // 100)):
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
        new_value = str(randint(s.MINIMUM_LETTER_VALUE, s.MAXIMUM_LETTER_VALUE))
        if new_value != current_value:
            temp_dna[index_to_change] = new_value
            break

def mix_dna(temp_dna, index_to_mix, generation):
    """
    param: Mixes the DNA with another DNA.
    type: list[str,...,[int]], int, int
    return: None
    """
    with open(s.GEN_FOLDER + str(generation) + '/dna_' + str(index_to_mix), 'r') as dna_file:
        donor_dna = list(dna_file.read().split(','))
        dna_file.close()
    # How many letters and operators we are going to mix.
    cross_length = randint(s.CROSSOVER_MIN_LENGTH, s.CROSSOVER_MAX_LENGTH) * 2
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
        with open(s.GEN_FOLDER + str(generation) + '/dna_' + str(current_gen_index), 'r') as dna_file:
            tmp_dna = list(dna_file.read().split(','))
        dna_file.close()
        if randint(1, 100) <= s.DNA_MUTATION_RATE:
            mutate_dna(tmp_dna)
        if randint(1, 100) <= s.DNA_MIX_RATE:
            while True:
                index_to_mix = generation_top_scores[randint(0, len(generation_top_scores) - 1)]
                if index_to_mix != current_gen_index:
                    break
            mix_dna(tmp_dna, index_to_mix, generation)
        with open(s.GEN_FOLDER + str(generation + 1) + '/dna_' + str(loop_index), 'w') as dna_file:
            dna_file.write(str(tmp_dna))
        dna_file.close()
        loop_index += 1

def complete_next_generation(generation, top_scores_length):
    """
    param: Completes the next generation with random DNAs.
    type: int, int
    return: None
    """
    for index_to_complete in range(top_scores_length, s.POPULATION_SIZE - 1):
        print("Completing DNA: " + str(index_to_complete) + " out of: " + str(s.POPULATION_SIZE))
        with open(s.GEN_FOLDER + str(generation + 1) + '/dna_' + str(index_to_complete), 'w') as dna_file:
            dna_file.write(str(get_dna()))
            dna_file.close()
    for member in range(s.POPULATION_SIZE):
        if not path.exists(s.GEN_FOLDER + str(generation) + '/dna_' + str(member)):
            with open(s.GEN_FOLDER + str(generation + 1) + '/dna_' + str(member), 'w') as dna_file:
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
    gen_folder = create_folder(s.GEN_FOLDER, 0)
    print("Creating cohort for generation 0")
    for member in range(s.POPULATION_SIZE):
        dna = get_dna()
        print("Generated DNA: " + str(member + 1) + " out of: " + str(s.POPULATION_SIZE))
        with open(gen_folder + '/dna_' + str(member), 'w') as dna_file:
            dna_file.write(str(dna))
            dna_file.close()
    # Assess each generation, get the healthiest DNAs and create the next generation.
    for generation in range(s.GENERATIONS):
        print("Working in generation: " + str(generation))
        # Create the sets for each DNA.
        for member in range(s.POPULATION_SIZE):
            with open(s.GEN_FOLDER + str(generation) + '/dna_' + str(member) + '_sets', 'w') as sets_file:
                for i in range(s.SET_SIZE):
                    line="" 
                    for number in range(s.SET_LENGTH):
                        line += str(calculate_digit(dna)) + ','
                    line = line[:-1] + '\n'
                    sets_file.write(line)
            sets_file.close()
        # Assess the sets and get the top scores.
        generation_top_scores = []
        current_gen_folder = gen_folder # This we learned from fibonacci()
        next_gen_folder = create_folder(s.GEN_FOLDER, generation + 1)
        gen_folder = next_gen_folder
        dna_scores = []
        for current_sets_file in range(s.POPULATION_SIZE - 1):
            with open (current_gen_folder + '/dna_' + str(current_sets_file) + '_sets', 'r') as sets_file:
                set_scores = []
                for set_line in sets_file:
                    set_line = set_line.strip()
                    set_scores.append(assess(list(set(set_line.split(',')))))
            sets_file.close()
            dna_scores.append(int(mean(set_scores)))
        generation_top_scores = get_top_scores(dna_scores)
        print("Top score: " + str(max(dna_scores)) + " Average score: " + str(mean(dna_scores)))
        with open (current_gen_folder + '/top_scores', 'w') as top_scores_file:
            score_index=0
            for score in generation_top_scores:
                top_scores_file.write(str(score_index) + ":" + str(score) + '\n')
                score_index += 1
        top_scores_file.close()
        print("Ascending top DNAs to the next generation.")
        ascend_dna(generation_top_scores, generation)
        print("Completing the next generation with new random DNAs.")
        complete_next_generation(generation, len(generation_top_scores))

if __name__ == '__main__':
    main()
