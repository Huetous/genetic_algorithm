from Utils import Utils
import numpy as np
import random
import matplotlib.pyplot as plt


class GeneticAlgorithm:
    def __init__(self, n_iters=100, early_stopping_rounds=10, eps=0.01,
                 verbose=0, plot_history=False):

        self.n_iters = n_iters
        self.early_stopping_rounds = early_stopping_rounds
        self.eps = eps

        self.verbose = verbose
        self.plot_history = plot_history

        self.is_fitted = False

        self.target_func = None
        self.generation = None
        self.n_descendants = None

        self.crossing = None
        self.mutation = None
        self.selection = None

    def create_next_generation(self, generation, n_descendants):
        new_generation = []  # Array for new individuals
        n_pairs = n_descendants // 2
        participants = list(range(len(generation)))

        for i in range(n_pairs):
            # Select individuals that were not crossed
            k, m = Utils.get_random_from_array(participants)
            x, y = generation[k], generation[m]

            # Remove selected individuals from crossing process
            participants.remove(k)
            participants.remove(m)

            # two new individuals
            a, b = self.crossing(x, y)
            new_generation.append(a)
            new_generation.append(b)

        return new_generation

    def fit(self, target_func, crossing, mutation, selection):

        if target_func is None:
            raise ValueError("Parameter <target_func> must be specified.")
        else:
            self.target_func = target_func

        if crossing is None:
            raise ValueError("Parameter <crossing> must be specified.")
        else:
            self.crossing = crossing

        if mutation is None:
            raise ValueError("Parameter <mutation> must be specified.")
        else:
            self.mutation = mutation

        if selection is None:
            raise ValueError("Parameter <selection> must be specified.")
        else:
            self.selection = selection

        self.is_fitted = True

        if self.verbose > 1:
            print("-" * 40)
            print(">   CONFIGURATION")
            print(f"\tTarget function: \t\t[{target_func.__name__}]")
            print(f"\tSelection method: \t\t[{selection.__name__}]")
            print(f"\tMutation method: \t\t[{mutation.__name__}]")
            print(f"\tCrossing method: \t\t[{crossing.__name__}]")
            print(f"\tNumber of iterations: \t[{self.n_iters}]")
            print(f"\tEarly stopping rounds: \t[{self.early_stopping_rounds}]")
            print(f"\tPrecision: \t\t\t\t[{self.eps}]")
            print("-" * 40)

        return self

    def compute(self, generation, n_descendants):
        if self.is_fitted is False:
            raise Exception("Method fit must be called first.")

        if generation is None:
            raise ValueError("Parameter <generation> must be specified.")
        else:
            self.generation = generation

        if n_descendants > len(generation):
            print("Parameter <n_descendants> must be less than len(generation).\n")

        result = {}
        if self.plot_history:
            result['history_y'] = []  # Array for max target function value on each iteration
            result['history_x'] = []  # Array for max target function value coordinate on each iteration

        prev_max_value = 0  # Max target function value from previous iteration
        iter_woi = 0  # Count for iterations without improvement

        result['max_value'] = 0  # Max target function value
        result['max_value_index'] = 0  # X coordinate on which max target function value is reached

        for i in range(self.n_iters):
            # NEW GENERATION
            new_generation = self.create_next_generation(generation, n_descendants)

            # Add new generation to existing one
            generation = list(np.concatenate([generation, new_generation]))
            random.shuffle(generation)

            # MUTATION
            size = len(generation)
            for j in range(size):
                generation[j] = self.mutation(generation[j])

            # SELECTION
            generation = self.selection(self.target_func, generation, n_descendants)

            # Find max target function value on this iteration and its index
            size = len(generation)
            for j in range(size):
                cached = self.target_func(generation[j])
                if abs(cached) > abs(result['max_value']):
                    result['max_value'] = cached
                    result['max_value_index'] = Utils.binary_to_decimal(generation[j])

            if self.verbose > 0:
                print(f"Iteration:\t{i}\tValue:\t{result['max_value']}")

            # Check if there are any improvements
            if abs(prev_max_value - result['max_value']) < self.eps:
                iter_woi += 1
                if iter_woi == self.early_stopping_rounds:
                    print("Early stopping. Iteration number:", i)
                    break
            else:
                iter_woi = 0

            prev_max_value = result['max_value']

            if self.plot_history:
                history_y.append(result['max_value'])
                history_x.append(Utils.binary_to_decimal(generation[result['max_value_index']]))
        if self.verbose > 0:
            print("-" * 40)

        if self.plot_history:
            result['history_x'] = history_x
            result['history_y'] = history_y
        return result
