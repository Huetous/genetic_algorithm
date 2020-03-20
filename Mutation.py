import numpy as np
from Utils import Utils


class Mutation:

    """
    Method: Invert Chromosome
    Inverts value of random chromosome
    """
    @staticmethod
    def invert_chromosome(x):
        i = np.random.randint(0, len(x) - 1)

        if x[i] == 1:
            x[i] = 0
        else:
            x[i] = 1

        return x

    """
    Method: Rearrange Chromosomes
    Rearranges two random chromosomes in places
    """
    @staticmethod
    def rearrange_chromosomes(x):
        i, j = Utils.get_random_from_bounds(0, len(x) - 1)

        t = x[i]
        x[i] = x[j]
        x[j] = t

        return x

    """
    Method: Reverse Subsequence
    Reverses the sequence relative to a random point
    """
    @staticmethod
    def reverse_subsequence(x):
        n = len(x)
        j = np.random.randint(0, n - 1)

        a = x[j:]
        a = list(reversed(a))
        x[j:] = a
        return x


