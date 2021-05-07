from model import Environment
import matplotlib.pyplot as plt
import numpy as np
import argparse

WIDTH = 26
HEIGHT = 26
STEPS = 2000
DECAY = 0.99
SIGMA = 0.5
STRENGTH = 4.5


def compute_then_plot(env, steps):
    raise NotImplementedError


def total_encounters(env):
    counter = 0

    for agent in env.schedule.agents:
        counter += agent.encounters
    return counter / 2


def plot_continuous(env, steps=1000):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    env.animate(ax)
    fig_num = plt.get_fignums()[0]

    for i in range(steps):
        if not plt.fignum_exists(fig_num):
            return False

        plt.title('iteration: ' + str(i))
        plt.pause(0.001)

        # take a step
        env.step()

        # store the state for animation
        env.animate(ax)
        try:
            fig.canvas.draw()
        except:
            print("Ended simulation.")
    return True


def parser():
    parser = argparse.ArgumentParser("run_simulation")
    parser.add_argument("-decay",
                        "--decay",
                        help="float (0, 1), the rate in which the pheromone decays.",
                        type=float,
                        required=False)
    parser.add_argument("-sigma",
                        "--sigma",
                        help="float (0, 1), sigma of the Gaussian convolution",
                        type=float,
                        required=False)
    parser.add_argument("-strength",
                        "--strength",
                        help="float, strength of pheromones (default = 4.5)",
                        type=float,
                        required=False)
    args = parser.parse_args()
    return args.decay or DECAY, args.sigma or SIGMA, args.strength or STRENGTH


def compute_no_plot(env, steps):
    for _ in range(steps):
        env.step()


def plot_col(df, col):
    plt.figure()
    plt.ylim([0, np.max(df[col])])
    plt.xlabel('iteration')
    plt.ylabel(col)
    df[col].plot()


def animate_distribution(path_lengths, steps):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(steps):
        ax.clear()
        t_data = path_lengths.loc[i]
        t_data = t_data[t_data != np.inf]
        t_data.hist(ax=ax)
        plt.pause(0.001)


if __name__ == '__main__':

    decay, sigma, strength = parser()

    env = Environment(width=WIDTH, height=HEIGHT, n_colonies=1, n_ants=40,
                      n_obstacles=30, decay=decay, sigma=sigma,
                      moore=False, pheromone_strength=strength)
    plot_continuous(env, STEPS)
