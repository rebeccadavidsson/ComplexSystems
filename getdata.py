from model import Environment
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import seaborn as sns
import pandas as pd
sns.set()


def get_iterations(env, steps):

    for iteration in range(steps):

        # take a step
        status = env.step()

        if status == "ended":
            break

    return iteration


def showplot(pheromone_strengths):
    plt.xlabel("Time")
    plt.ylabel("Number of ants on track")
    plt.title("Convergence behavior of ants (n=30)")
    plt.legend(pheromone_strengths)
    plt.show()


def plot3d(width, height, steps, n, decays, sigmas, pheromone_strength):
    df = pd.DataFrame(columns=["decay", "sigma", "strength", "iteration"])
    row = 0
    decay = 0

    for decay in decays:
        for sigma in sigmas:
            for strength in pheromone_strength:
                print(decay, sigma, strength)
                env = Environment(width=width, height=height, n_colonies=1,
                                  n_ants=30, n_obstacles=10, decay=decay, sigma=sigma,
                                  moore=False, pheromone_strength=strength)

                iter = get_iterations(env, steps)
                df.loc[row] = [decay, sigma, strength, iter]
                row += 1
            decay += 1
    return df


def plot2d(width, height, steps, n, decays, sigmas, strength):
    df = pd.DataFrame(columns=["decay", "sigma", "iteration"])
    row = 0

    for decay in decays:
        for sigma in sigmas:
            print(decay, sigma)
            env = Environment(width=width, height=height, n_colonies=1,
                              n_ants=30, n_obstacles=10, decay=decay, sigma=sigma,
                              moore=False, pheromone_strength=strength)

            iter = get_iterations(env, steps)
            df.loc[row] = [decay, sigma, iter]
            row += 1
    return df


if __name__ == '__main__':
    width = 26
    height = 26
    steps = 1300
    n = 20
    decays = np.linspace(0.7, 0.99, num=n)
    sigmas = np.linspace(0.01, 0.6, num=n)
    pheromone_strengths = np.linspace(1, 15, num=n)

    for strength in pheromone_strengths:
        df = plot2d(width, height, steps, n, decays, sigmas, strength)
        # df = plot3d(width, height, steps, n, decays, sigmas, pheromone_strengths)
        df.to_pickle("./df_heatmapMP4" + strength + ".pkl")
