from numpy import append, array

from assess_set_line import assess_dna


def call_assess_dna(current_gen_folder, current_file_index, scores_file):
    with open(current_gen_folder + '/dna_' + str(current_file_index) + '_sets', 'r') as sets_file:
        print("Assessing sets for member: " + str(current_file_index + 1))
        set_scores = array([])
        for set_line in sets_file:
            set_line = set_line.strip()
            line_set = list(set(set_line.split(',')))
            line_score = assess_dna(line_set)
            if line_score == 0 or line_score is None:
                set_scores = append(set_scores, [current_file_index, 0])
            else:
                set_scores = append(set_scores, [current_file_index, line_score])
    sets_file.close()
    scores_file.write(current_file_index + "," + int(set_scores[:, 1].mean()))
    scores_file.flush()
