import numpy as np
from Utils import Utils


class Crossing:

    """
    Method: Single Point
    Randomly selects one chromosome and all the chromosomes that go after
    this one, swaps with the corresponding ones in another individual
    Returns: two new individuals
    """
    @staticmethod
    def single_point(x, y):
        # Copy given individuals
        left = x.copy()
        right = y.copy()

        i = np.random.randint(0, len(x) - 1)

        # Swap segments
        t = left[i:]
        left[i:] = right[i:]
        right[i:] = t

        return left, right

    """
    Method: Double Point
    Performs single point crossing successive two times
    """
    @staticmethod
    def double_point(x, y):
        left = x.copy()
        right = y.copy()

        i, j = Utils.get_random_from_bounds(0, len(x) - 1)
        if i < j:
            t = i
            i = j
            j = t

        t = left[i:]
        left[i:] = right[i:]
        right[i:] = t

        t = left[j:i]
        left[j:i] = right[j:i]
        right[j:i] = t

        return left, right


    @staticmethod
    def universal(x, y, prob=0.5):
        left = x.copy()
        right = y.copy()
        n = len(x)
        z = [list(np.zeros(n)), list(np.zeros(n))]

        for j in range(2):
            for i in range(n):
                val = np.random.uniform(0, 1)
                if val >= prob:
                    z[j][i] = x[i]
                else:
                    z[j][i] = y[i]

        return z[0], z[1]

    @staticmethod
    def homogeneous(x, y):
        n = len(x)
        z = [list(np.zeros(n)), list(np.zeros(n))]
        for j in range(2):
            mask = np.random.randint(0, 2, n)
            for i in range(n):
                if mask[i] == 0:
                    z[j][i] = x[i]
                else:
                    z[j][i] = y[i]
        return z[0], z[1]


