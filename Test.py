import numpy as np
import matplotlib.pyplot as plt

from GeneticAlgorithm import GeneticAlgorithm
from Selection import Selection
from Crossing import Crossing
from Mutation import Mutation
from Utils import Utils

N_INDIVIDUALS = 20  # Size of generation on each iteration
N_CHROMOSOME = 10  # Length of array which represents an individual
N_DESCENDANTS = 10

# Domain of definition of polynomial
START = 0
END = 35

N_ITERS = 100  # Number of iterations of algorithm

# Stop computing if there are EARLY_STOPPING_ROUNDS iterations
# without improvement
EARLY_STOPPING_ROUNDS = 5
EPS = 0.01  # Precision of computing

# Polynomial for
def polynomial(x):
    # return (np.sin(x - 2) * np.cos(x + 4) + np.cos(3 * x)) * x ** 2
    return (x - 3) * (x - 15) * (x - 0.5) * (x - 24) * (x - 6) * np.sin(x)


def target_func(x):
    v = Utils.binary_to_decimal(x)

    # Scale x from [START, END] to [0, 2**N_CHROMOSOME]
    v *= END
    v /= 2 ** N_CHROMOSOME - 1
    v = polynomial(v)
    return v


# Plot graph of polynomial
def plot():
    x = np.linspace(START, END, 300)
    y = [polynomial(x_) for x_ in x]

    plt.plot(y)
    plt.show()


# Create first generation
def init():
    x = np.random.randint(START, 2 ** N_CHROMOSOME, N_INDIVIDUALS)
    gen = []
    for i in range(N_INDIVIDUALS):
        v = Utils.decimal_to_binary(x[i], N_CHROMOSOME)
        v = Utils.string_to_array(v)
        gen.append(v)
    return gen

# Finds an extremum and coordinate at which it is reached
def get_real_ext():
    n = 1000
    h = (END - START) / n

    max = 0
    max_ind = 0
    for i in range(n):
        val = polynomial(i * h)
        if val > max:
            max = val
            max_ind = i

    max_ind *= h
    return max, max_ind


def main():
    gen = init()  # Create initial generation

    # Four crossing schemes are available
    crossing = Crossing.single_point
    # crossing = Crossing.double_point
    # crossing = Crossing.universal
    # crossing = Crossing.homogeneous

    # Three mutation schemes are available
    mutation = Mutation.invert_chromosome
    # mutation = Mutation.revers_rand_subseq
    # mutation = Mutation.perm_rand_chromo

    # Four selection schemes are available
    selection = Selection.random_scheme
    # selection = Selection.tournament_scheme
    # selection = Selection.roulette_scheme
    # selection = Selection.truncation_scheme

    params = {
        "n_iters": N_ITERS,
        "early_stopping_rounds": EARLY_STOPPING_ROUNDS,
        "eps": EPS,
        "verbose": 0,
        "plot_history": False
    }

    ga = GeneticAlgorithm(**params).fit(target_func=target_func,
                                        crossing=crossing,
                                        mutation=mutation,
                                        selection=selection)
    ext, x = ga.compute(gen, N_DESCENDANTS)

    # Scale x from [0, 2**N_CHROMOSOME] to [START, END]
    x *= END
    x /= 2 ** N_CHROMOSOME - 1

    # Find real extremum and coordinate at which it is reached
    real, real_ind = get_real_ext()

    print("Real extremum value:", real)
    print("Value found by algorithm: ", ext)
    print("Error: ", abs(real - ext))
    print("X coordinate: ", x)


# plot()
main()
