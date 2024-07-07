#!/usr/bin/python

from multiprocessing import Pool
from numpy import mean
from os import path
from sys import exit
from time import time

import settings as S
from core_count import core_count
from ascend_dna import ascend_dna
from assess_set_line import assess_set_line
from create_folder import create_folder
from create_sets import create_sets
from generate_member import generate_member
from get_top_scores import get_top_scores

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
    CORE_COUNT = core_count()
    # Create the first generation.
    gen_folder = create_folder(S.GEN_FOLDER, 0)
    print("Creating members for generation 0")
    start = time()
    pool = Pool(processes=CORE_COUNT)
    member = 0
    for member in range(S.POPULATION_SIZE):
        pool.apply_async(generate_member, args=(member, gen_folder))
    pool.close()
    pool.join()
    print("Generation 0 was created in " + str(time()-start) + " seconds.")
    # Assess each generation, get the healthiest DNAs and create the next generation.
    for generation in range(S.GENERATIONS):
        gen_time = time()
        print("Working in generation: " + str(generation))
        # Create the sets for each DNA.
        print("Creating sets for generation " + str(generation))
        start = time()
        pool = Pool(processes=CORE_COUNT)
        member = 0
        for member in range(S.POPULATION_SIZE):
            pool.apply_async(create_sets, args=(generation, member,))
        pool.close()
        pool.join()
        print("Creating sets took " + str(time()-start) + " seconds.")
        # Assess the sets and get the top scores.
        print("Assessing the sets and getting the top performers.")
        generation_top_scores = []
        current_gen_folder = gen_folder
        next_gen_folder = create_folder(S.GEN_FOLDER, generation + 1)
        gen_folder = next_gen_folder
        dna_scores = []
        start = time()

        for current_sets_file_index in range(S.POPULATION_SIZE):
            sets_file_path = current_gen_folder + '/dna_' + str(current_sets_file_index) + '_sets'
            scores_file_path = current_gen_folder + '/dna_' + str(current_sets_file_index) + '_scores'
            mean_file_path = current_gen_folder + '/dna_' + str(current_sets_file_index) + '_mean'
            with open(sets_file_path, 'r') as sets_file:
                print("Assessing sets for member: " + str(current_sets_file_index + 1))
                set_scores = []
                for set_line in sets_file:
                    set_line = set_line.strip()
                    assessment = assess_set_line(list(set(set_line.split(','))))
                    if assessment is None or assessment == 0:
                        set_scores.append(0)
                    else:
                        set_scores.append(assessment)
                with open(scores_file_path, 'w') as scores_file:
                    scores_file.write(str(set_scores) + "," + str(current_sets_file_index))
                    scores_file.close()
            sets_file.close()
            mean_score = mean(set_scores)
            try:
                dna_scores.append(int(mean_score))
            except TypeError:
                dna_scores.append(0)
            with open(mean_file_path, 'w') as mean_file:
                mean_file.write(str(int(mean_score)))
                mean_file.close()

        print("Assessing DNAs took " + str(time()-start) + " seconds.")
        start = time()
        # Generating the top score indices for this generation.
        generation_top_scores = get_top_scores(current_gen_folder)
        print("Top score: " + str(max(dna_scores)) + " Average score: " + str(mean(dna_scores)))
        with open(current_gen_folder + '/top_scores', 'w') as top_scores_file:
            score_index = 0
            for score in generation_top_scores:
                top_scores_file.write(str(score_index) + ":" + str(score) + '\n')
                score_index += 1
        top_scores_file.close()
        print("Getting top scores took " + str(time()-start) + " seconds.")
        print("Ascending top DNAs to the next generation.")
        ascend_dna(generation_top_scores, generation)
        print("Completing the next generation with new random DNAs.")
        start = time()
        pool = Pool(processes=core_count())
        member = 0
        for member in range(len(generation_top_scores), S.POPULATION_SIZE):
            pool.apply_async(generate_member, args=(member, next_gen_folder))
        pool.close()
        pool.join()
        print("Completing next generation took" + str(time()-start) + " seconds.")
        print("Generation " + str(generation) + " took " + str(time()-gen_time) + " seconds.")


if __name__ == '__main__':
    main()
