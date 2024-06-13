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
GENERATIONS = 10             # How many generations are there in a simulation.
SET_LENGTH = 10              # How many digits in a set.

"""
SET_SIZE means how many lines of sets are there for a given DNA. This is also how many times the DNA
is tested to see if it can generate a number between MINIMUM_DIGIT and MAXIMUM_DIGIT. If it can, then
it is considered healthy.
Too small a size will not give good results, and too large a size will take a very long time to generate.
"""
SET_SIZE = 100              # How many sets each DNA generates. Also how many tests each DNA has to pass.

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
SET_HEALTH = 95
GEN_FOLDER = "generation-"   # The folder name for each generation.
TEST_FILE = "test.csv"       # The file that contains the test sets.


"""
Parameters for generational changes:
"""
ASCENDING = 50               # Percentage of top DNAs that are taken from the previous generation.
DNA_MUTATION_RATE = 1        # Percentage of the DNA that is mutated.
DNA_MIX_RATE = 10            # Percentage of the DNAs that mix together (sort of sexual reproduction).
DNA_DUPLICATION_RATE = 1     # Percentage of the DNAs that will have some of their instructions duplicated.
DNA_REDUCTION_RATE = 1       # Percentage of the DNAs that will have some of their instructions removed.

"""
CHANGE_MIN/MAX is used when the script wants to do things like duplicating existing instructions,
removing a length of instructions or taking some instructions from a different DNA.
The length is a pair of a number (letter) plus an operator.
"""
CHANGE_MIN_LENGTH = 1        # Minimum length of pairs to change.
CHANGE_MAX_LENGTH = 3        # Maximum length of pairs to change.

"""
Free threads  that are kept for other operations. This is used so that the code won't choke the CPU.
"""
FREE_THREADS = 2
