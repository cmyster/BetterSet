#!/usr/bin/python

import settings as S
from random import randint
with open('./test.csv', 'w') as f:
    for i in range(S.SET_SIZE):
        line=[]
        for j in range(S.SET_LENGTH):
            line.append(str(randint(S.MINIMUM_DIGIT, S.MAXIMUM_DIGIT)))
        line.pop()
        f.write(','.join(line) + '\n')
f.close()
            
