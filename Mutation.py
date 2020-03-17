import numpy as np
from Utils import Utils


class Mutation:
    @staticmethod
    def rand_single_chromo(x):
        i = np.random.randint(0, len(x) - 1)

        if x[i] == 1:
            x[i] = 0
        else:
            x[i] = 1

        return x

    @staticmethod
    def perm_rand_chromo(x):
        i, j = Utils.get_random_from_bounds(0, len(x) - 1)

        t = x[i]
        x[i] = x[j]
        x[j] = t

        return x

    @staticmethod
    def revers_rand_subseq(x):
        n = len(x)
        j = np.random.randint(0, n - 1)

        a = x[j:]
        a = list(reversed(a))
        x[j:] = a
        return x


