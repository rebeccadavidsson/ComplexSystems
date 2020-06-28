from model import Environment
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import seaborn as sns
import pickle
sns.set()


def get_iterations(env, steps):

    for iteration in range(steps):

        # take a step
        status = env.step()

        if status == "ended":
            break

    return iteration


def run_continuous(env, steps=1000):

    nr_on_track = []

    for i in tqdm(range(steps)):

        # take a step
        env.step()

        ratio = env.calc_ratio()
        nr_on_track.append(ratio[0])

    return nr_on_track


def plot_ratio(env, steps):
    nr_on_track = run_continuous(env, steps)
    plt.plot(np.arange(0, steps), nr_on_track)


def showplot(pheromone_strengths, total, steps):

    for values in total:
        plt.plot(np.arange(0, steps), values)

    plt.xlabel("Time")
    plt.ylabel("Number of ants on track")
    plt.title("Convergence behavior of ants (n=30)")
    plt.legend(pheromone_strengths)
    plt.show()


if __name__ == '__main__':
    width = 26
    height = 26
    steps = 1500
    ant_size = 0.4
    n = 40
    pheromone_strengths = np.linspace(0.7, 2.7, num=n)
    loops = 30

    total = []
    for value in pheromone_strengths:
        averages = []
        env = Environment(width=width, height=height, n_colonies=1, n_ants=30, n_obstacles=20, decay=0.99, sigma=0.12,
                          moore=False, pheromone_strength=value)
        nr_iterations = get_iterations(env, steps)
        total.append(nr_iterations)

    with open('data/plot_runs.pkl', 'wb') as f:
        pickle.dump(total, f)
