import random, math
import numpy as np
from Utils import Utils


class Selection:
    """
    Method: Random Scheme
    Randomly removes n_descendants individuals from given generation
    """
    @staticmethod
    def random_scheme(target_func, generation, n_descendants):
        n = len(generation)
        for i in range(n_descendants):
            k, _ = Utils.get_random_from_bounds(0, n - 1)
            del generation[k]
            n -= 1
        return generation

    """
    Method: Roulette Scheme
    Removes n_descendants individuals from given generation as follows:
    1) Find sum of target values of all generation
    2) Check if value of particular individual is lying within [a,b],
        where a,b - two random points from [0, 2Pi]
    3) If its not - delete it
    """
    @staticmethod
    def roulette_scheme(target_func, generation, n_descendants):
        target_values = [target_func(x) for x in generation]
        sum_target_values = np.sum(target_values)

        n = len(generation)
        deleted = 0
        while deleted < n_descendants:
            k, _ = Utils.get_random_from_bounds(0, n - 1)

            value = 2 * np.pi * target_values[k]
            value /= sum_target_values

            a, b = Utils.get_random_from_bounds(0, 2 * np.pi, int=False)
            if a > b:
                a, b = b, a

            n -= 1

            # if the value is not included in the segment
            # then delete this individual from generation
            if not a <= value <= b:
                del generation[k]
                deleted += 1
        return generation

    """
    Method: Tournament Scheme
    Removes n_descendants individuals from given generation as follows:
    1) Select two individuals
    2) Compare them by target function
    3) Remove one with lower target function value
    """
    @staticmethod
    def tournament_scheme(target_func, generation, n_descendants):
        n = len(generation)
        for i in range(n_descendants):
            k, m = Utils.get_random_from_bounds(0, n - 1)
            x_val = target_func(generation[k])
            y_val = target_func(generation[m])

            n -= 1

            # delete from generation individual with lower target function value
            if abs(x_val) > abs(y_val):
                del generation[m]
            else:
                del generation[k]

        return generation

    """
    Method: Truncation Scheme
    Removes n_descendants individuals from given generation as follows:
    1) Sort individuals in generation by target function values
    2) Remove last n_descendants individuals
    """
    @staticmethod
    def truncation_scheme(target_func, generation, n_descendants):
        # Sort by decreasing absolute target function value
        generation.sort(key=lambda x: abs(target_func(x)), reverse=True)

        # Cut off last n_descendants individuals
        return generation[:len(generation) - n_descendants]

