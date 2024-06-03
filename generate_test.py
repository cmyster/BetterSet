#!/usr/bin/python

from random import randint
with open('./test.csv', 'w') as f:
    for i in range(1000):
        line=[]
        for j in range(10):
            line.append(str(randint(1, 50)))
        line.pop()
        f.write(','.join(line) + '\n')
f.close()
            