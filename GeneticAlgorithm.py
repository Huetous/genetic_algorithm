from Utils import Utils
import numpy as np
import random
import matplotlib.pyplot as plt


class GeneticAlgorithm:
    def __init__(self, target_func=None,
                 crossing=None, mutation=None, selection=None,
                 generation=None, n_descendants=10,
                 n_iters=100, early_stopping_rounds=10, eps=0.01,
                 verbose=0, plot_history=False):

        if target_func is None:
            raise ValueError("Parameter <target_func> must be specified.")
        else:
            self.target_func = target_func

        if n_descendants > len(generation):
            print("Parameter <n_descendants> must be less than len(generation).\n")
        else:
            self.n_descendants = n_descendants

        if generation is None:
            raise ValueError("Parameter <generation> must be specified.")
        else:
            self.generation = generation

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

        self.n_iters = n_iters
        self.early_stopping_rounds = early_stopping_rounds
        self.eps = eps

        self.verbose = verbose
        self.plot_history = plot_history

        if verbose > 1:
            print("-" * 40)
            print(">   CONFIGURATION")
            print(f"\tTarget function: \t\t[{target_func.__name__}]")
            print(f"\tGeneration size: \t\t[{len(generation)}]")
            print(f"\tSelection method: \t\t[{selection.__name__}]")
            print(f"\tMutation method: \t\t[{mutation.__name__}]")
            print(f"\tCrossing method: \t\t[{crossing.__name__}]")
            print(f"\tNumber of descendants: \t[{n_descendants}]")
            print(f"\tNumber of iterations: \t[{n_iters}]")
            print(f"\tEarly stopping rounds: \t[{early_stopping_rounds}]")
            print(f"\tPrecision: \t\t\t\t[{eps}]")
            print(f"\tVerbose: \t\t\t\t[{verbose}]")
            print(f"\tPlot history: \t\t\t[{plot_history}]")
            print("-" * 40)

    def create_next_generation(self):
        had_child = np.zeros(len(self.generation))
        new_generation = []  # Array for new individuals
        n_pairs = self.n_descendants // 2
        n = len(self.generation)

        for i in range(n_pairs):
            # Select individuals that were not crossed
            k, m = Utils.get_random_from_bounds(0, n - 1)
            while had_child[k] == 1 or had_child[m] == 1:
                k, m = Utils.get_random_from_bounds(0, n - 1)

            had_child[k] = 1
            had_child[m] = 1
            x, y = self.generation[k], self.generation[m]

            # two new individuals
            a, b = self.crossing(x, y)
            new_generation.append(a)
            new_generation.append(b)

        return new_generation

    def compute(self):
        if self.plot_history:
            history_y = []  # Array for max target function value on each iteration
            history_x = []  # Array for max target function value coordinate on each iteration

        prev_max_value = 0  # Max target function value from previous iteration
        iter_woi = 0  # Count for iterations without improvement

        max_value = 0  # Max target function value
        max_value_index = 0  # X coordinate on which max target function value is reached

        for i in range(self.n_iters):
            # NEW GENERATION
            new_generation = self.create_next_generation()

            # Add new generation to existing one
            self.generation = list(np.concatenate([self.generation, new_generation]))
            random.shuffle(self.generation)

            # MUTATION
            size = len(self.generation)
            for j in range(size):
                self.generation[j] = self.mutation(self.generation[j])

            # SELECTION
            self.generation = self.selection(self.target_func, self.generation, self.n_descendants)

            # Find max target function value on this iteration and its index
            size = len(self.generation)
            for j in range(size):
                cached = self.target_func(self.generation[j])
                if abs(cached) > abs(max_value):
                    max_value = cached
                    max_value_index = Utils.binary_to_decimal(self.generation[j])

            if self.verbose > 0:
                print(f"Iteration:\t{i}\tValue:\t{max_value}")

            # Check if there are any improvements
            if abs(prev_max_value - max_value) < self.eps:
                iter_woi += 1
                if iter_woi == self.early_stopping_rounds:
                    print("Early stopping. Iteration number:", i)
                    break

            prev_max_value = max_value

            if self.plot_history:
                history_y.append(max_value)
                history_x.append(Utils.binary_to_decimal(self.generation[max_value_index]))
        if self.verbose > 0:
            print("-" * 40)

        if self.plot_history:
            plt.plot(history_y)
            plt.xlabel("Iteration Number")
            plt.ylabel("Target function value")
            plt.show()
            plt.plot(history_x)
            plt.xlabel("Iteration Number")
            plt.ylabel("X coordinate")
            plt.show()
        return max_value, max_value_index
