# TODO

1. Instead of picking the top performing DNAs, use logarithmic distribution to have more of the
   better-performing DNAs and less of the less-performing ones.
2. Calculations are linear:
    a. Assessing function needs to be multi-processed as well.
    b. Some calculations should be vectorized.
3. Needs a way to continue where we stopped:
   When we start, we start by checking which generations are there.
   If there are already generational folders, make sure they have all the files and continue.