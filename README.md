# Better Set

This is a educational program that I use to learn the basics of evolution.

It is using a CSV file with possible outcomes, and each generation uses
simple arithmetics and some randomness to try and achieve the same set
of numbers or something close to them.

All relevant settings are in the `settings.py` file.

It scores each "DNA" based on how many sets it created that have the same digits
as the ones in the test file.

Every generation, the most successful DNAs will be used, some merged, some mutated,
to create the next generation.

The end goal of the game is to create an instruction set  that will generate sets
of numbers in predictable way. If your test files contains random numbers, then the
instructions will eventually, given enough time, create random numbers as well in
the given range.

Example of a test file (you can use generate_test.py):

`1,2,3,4,5,6,7,8,9,10`
`2,3,4,5,6,7,8,9,10,11`
`3,4,5,6,7,8,9,10,11,12`
`...`

Example of a 'DNA':
Pairs of numbers and operators, the last element is a list of indices that will be randomly
modified.
`['5', '-', '2', '*', '2', '-', '3', '/', '2', [0, 2]]`
