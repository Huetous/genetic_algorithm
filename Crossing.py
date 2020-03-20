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
        a = x.copy()
        b = y.copy()

        i = np.random.randint(0, len(x) - 1)

        # Swap segments
        t = a[i:]
        a[i:] = b[i:]
        b[i:] = t

        return a, b

    """
    Method: Double Point
    Performs single point crossing successive two times
    """

    @staticmethod
    def double_point(x, y):
        a = x.copy()
        b = y.copy()

        i, j = Utils.get_random_from_bounds(0, len(x) - 1)
        if i < j:
            t = i
            i = j
            j = t

        t = a[i:]
        a[i:] = b[i:]
        b[i:] = t

        t = a[j:i]
        a[j:i] = b[j:i]
        b[j:i] = t

        return a, b

    """
    Method: Universal
    Creates two new individuals as follows:
    On each iteration:
    1) Get a value from (0,1)
    2) if value > given prob then take a chromosome from first individual
    otherwise - from another
    """

    @staticmethod
    def universal(x, y, prob=0.5):
        n = len(x)
        a = np.zeros(n)
        b = np.zeros(n)

        for t in [a, b]:
            for i in range(n):
                val = np.random.uniform(0, 1)
                if val >= prob:
                    t[i] = x[i]
                else:
                    t[i] = y[i]

        return a, b

    """
    Method: Homogeneous
    Creates two new individuals as follows:
    1) For each new individuals create a mask (eg, [0,1,1,1])
    2) if mask[i] == 0 then take a chromosome from first individuals
    otherwise - from another
    """

    @staticmethod
    def homogeneous(x, y):
        n = len(x)
        a = np.zeros(n)
        b = np.zeros(n)
        for t in [a, b]:
            mask = np.random.randint(0, 2, n)
            for i in range(n):
                if mask[i] == 0:
                    t[i] = x[i]
                else:
                    t[i] = y[i]
        return a, b
