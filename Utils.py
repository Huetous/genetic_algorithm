import random


class Utils:

    #  Return two random elements from give array
    @staticmethod
    def get_random_from_array(A):
        i, j = Utils.get_random_from_bounds(0, len(A) - 1)
        return A[i], A[j]

    # Return two not equal indices from given segment
    @staticmethod
    def get_random_from_bounds(a, b, int=True):
        x = y = a

        if int:
            rnd = lambda a, b: random.randint(a, b)
        else:
            rnd = lambda a, b: random.uniform(a, b)

        while x is y:
            x = rnd(a, b)
            y = rnd(a, b)
        return x, y

    @staticmethod
    def decimal_to_binary(n, l):
        return bin(n).replace("0b", "").zfill(l)

    @staticmethod
    def string_to_array(s):
        a = []
        for i in range(len(s)):
            a.append(int(s[i]))
        reversed(a)
        return a

    @staticmethod
    def binary_to_decimal(n):
        s = ""
        reversed(n)
        for i in range(len(n)):
            s += str(n[i])
        return int(s, 2)
