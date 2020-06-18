from model import Environment
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import seaborn as sns
sns.set()


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


def showplot(pheromone_strengths):
    plt.xlabel("Time")
    plt.ylabel("Number of ants on track")
    plt.title("Convergence behavior of ants (n=30)")
    plt.legend(pheromone_strengths)
    plt.show()


if __name__ == '__main__':
    width = 26
    height = 26
    steps = 1000
    ant_size = 0.4
    pheromone_strengths = [1, 10, 100]
    loops = 4

    for value in pheromone_strengths:
        averages = []
        for i in range(loops):
            env = Environment(width=width, height=height, n_colonies=1, n_ants=30, n_obstacles=10, decay=0.99, sigma=0.2,
                              moore=False, pheromone_strength=value)
            nr_on_track = run_continuous(env, steps)
            averages.append(nr_on_track)
        average = list(map(lambda x: sum(x)/len(x), zip(*averages)))
        plt.plot(np.arange(0, steps), average)

    showplot(pheromone_strengths)
