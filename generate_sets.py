#!/usr/bin/python

from os import path
from sys import argv
from ast import literal_eval

import settings as S
import calculate_digit as cd

"""
This script gets a "DNA" file and generates a set of numbers based on the DNA.
type: str (path to file), int (number of sets to generate), int (number of digits in a set)
returns: stdio (prints the generated sets)
"""

HELP = "Usage: python generate_sets.py --file=<DNA file path>\nOPTIONAL: --sets=<number of sets>\n          --digits=<number of digits in a set>"


def main():
    if len(argv) < 2:
        print(HELP)
        return

    if argv[1] == "--help":
        print(HELP)
        return

    size = S.SET_SIZE
    length = S.SET_LENGTH

    for arg in argv[1:32]:
        if "--file=" in arg:
            dna_file = arg.split("=")[1]
            if not path.exists(dna_file):
                print("File does not exist: ", dna_file)
                return
        else:
            print(HELP)
            return
        if "--sets=" in arg:
            size = int(arg.split("=")[1])
        if "--digits=" in arg:
            length = int(arg.split("=")[1])

    dna = []
    with open(dna_file, "r") as f:
        dna = literal_eval(f.read())
    f.close()

    for i in range(size):
        line = ""
        for j in range(length):
            line += str(cd.calculate_digit(dna)) + ","
        print(line[:-1])    


if __name__ == "__main__":
    main()
