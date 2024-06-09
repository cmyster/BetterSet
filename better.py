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
modified.
['5', '-', '2', '*', '2', '-', '3', '/', '2', [0, 2]]

TODO:
1. Instead of picking the top performing DNAs, use logarithmic distribution to have more of the
   better-performing DNAs and less of the less-performing ones.
2. Calculations are linear:
    a. Some functions can be delegated to different threads. This needs a waiter function.
    b. Some calculations should be vectorized.
3. Parts of the DNA can also be duplicated and/or reduced in length (repetitions).
"""

from numpy import mean
from os import path
from random import randint, randrange

import settings as S
from create_sets import create_sets
from get_dna import get_dna
from create_folder import create_folder
from assess_dna import assess
from top_scores import get_top_scores
from ascend_dna import ascend_dna
from complete_next_gen import complete_next_generation

if not path.exists(S.TEST_FILE):
    print("Test file not found.")
    exit(1)

def main():
    """
    param: Main function, creates "healthy" DNAs for gen-0 and their files. gen-1+ will be generated from gen-0.
    Calculating stuff happens elsewhere.
    type: None
    return: None
    """
    # Create the first generation.
    gen_folder = create_folder(S.GEN_FOLDER, 0)
    print("Creating cohort for generation 0")
    for member in range(S.POPULATION_SIZE):
        dna = get_dna(member)
        with open(gen_folder + '/dna_' + str(member), 'w') as dna_file:
            dna_file.write(str(dna))
            dna_file.close()
    # Assess each generation, get the healthiest DNAs and create the next generation.
    for generation in range(S.GENERATIONS):
        print("Working in generation: " + str(generation))
        # Create the sets for each DNA.
        print("Creating sets for this generation.")
        for member in range(S.POPULATION_SIZE):
            create_sets(generation, dna)
        # Assess the sets and get the top scores.
        print("Assessing the sets and getting the top performers.")
        generation_top_scores = []
        current_gen_folder = gen_folder # This we learned from fibonacci()
        next_gen_folder = create_folder(S.GEN_FOLDER, generation + 1)
        gen_folder = next_gen_folder
        dna_scores = []
        for current_sets_file in range(S.POPULATION_SIZE - 1):
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
