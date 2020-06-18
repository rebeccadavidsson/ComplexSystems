from model import Environment
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set()


def run_continuous(env, steps=1000):

    nr_on_track, nr_of_track = [], []

    for i in range(steps):

        if i % 100 == 0:
            print("Step: ", i, "out of ", steps)
        # take a step
        env.step()

        ratio = env.calc_ratio()
        nr_on_track.append(ratio[0])
        nr_of_track.append(ratio[1])

    return nr_on_track, nr_of_track


def plot_ratio(env, steps):

    time = np.arange(0, steps)
    nr_on_track, nr_of_track = run_continuous(env, steps)
    plt.plot(time, nr_on_track)
    plt.plot(time, nr_of_track)
    plt.legend(["On track", "Not on track"])
    plt.show()


if __name__ == '__main__':
    width = 26
    height = 26
    steps = 1000
    ant_size = 0.4

    env = Environment(width=width, height=height, n_colonies=1, n_ants=30, n_obstacles=10, decay=0.99, sigma=0.2,
                      moore=False, pheromone_strength=10)
    plot_ratio(env, steps)
