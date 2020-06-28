from model import Environment
import matplotlib.pyplot as plt
import numpy as np



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
        if not plt.fignum_exists(fig_num): return False

        plt.title('iteration: ' + str(i))
        plt.pause(0.001)

        # take a step
        env.step()

        # store the state for animation
        env.animate(ax)
        fig.canvas.draw()
    return True


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
    width = 26
    height = 26
    steps = 2000
    ant_size = 0.4


    env = Environment(width=width, height=height, n_colonies=1, n_ants=30, n_obstacles=50, decay=0.99, sigma=0.5,
                      moore=False, pheromone_strength=4.5)
    plot_continuous(env, steps)