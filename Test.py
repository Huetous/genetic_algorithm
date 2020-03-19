import numpy as np
import matplotlib.pyplot as plt

from GeneticAlgorithm import GeneticAlgorithm
from Selection import Selection
from Crossing import Crossing
from Mutation import Mutation
from Utils import Utils

N_INDIVIDUALS = 20  # Size of generation on each iteration
N_CHROMOS = 10  # Length of array which represents an individual
N_DESCENDANTS = 10

# Domain of definition of polynom
START = 0
END = 35

N_ITERS = 100  # Number of iterations of algorithm

# Stop computing if there are EARLY_STOPPING_ROUNDS iterations
# without improvement
EARLY_STOPPING_ROUNDS = 5
EPS = 0.01  # Precision of computin


def polynom(x):
    # return (np.sin(x - 2) * np.cos(x + 4) + np.cos(3 * x)) * x ** 2
    return (x - 3) * (x - 15) * (x - 0.5) * (x - 24) * (x - 6) * np.sin(x)


def target_func(x):
    v = Utils.binary_to_decimal(x)

    # Scale x from [START, END] to [0, 2**N_CHROMOS]
    v *= END
    v /= 2 ** N_CHROMOS - 1
    v = polynom(v)
    return v


# Plot graph of polynom
def plot():
    x = np.linspace(START, END, 300)
    y = [polynom(x_) for x_ in x]

    plt.plot(y)
    plt.show()


# Create first generation
def init():
    x = np.random.randint(START, 2 ** N_CHROMOS, N_INDIVIDUALS)
    gen = []
    for i in range(N_INDIVIDUALS):
        v = Utils.decimal_to_binary(x[i], N_CHROMOS)
        v = Utils.string_to_array(v)
        gen.append(v)
    return gen


def main():
    gen = init()

    crossing = Crossing.single_point
    # crossing = Crossing.double_point
    # crossing = Crossing.universal
    # crossing = Crossing.homogeneous

    mutation = Mutation.rand_single_chromo
    # mutation = Mutation.revers_rand_subseq
    # mutation = Mutation.perm_rand_chromo

    # selection = Selection.random_scheme
    # selection = Selection.tournament_scheme
    # selection = Selection.roulette_scheme
    selection = Selection.truncation_scheme

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

    # Scale x from [0, 2**N_CHROMOS] to [START, END]
    x *= END
    x /= 2 ** N_CHROMOS - 1

    # Find 'real' extremum
    z = np.linspace(START, END, 300)
    z = [polynom(z_) for z_ in z]
    real = max(z, key=lambda x: abs(x))

    print("Real extremum value:", real)
    print("Value found by algorithm: ", ext)
    print("Error: ", abs(real - ext))
    print("X coordinate: ", x)


# plot()
main()
