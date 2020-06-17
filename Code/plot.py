# -*- coding: utf-8 -*-
"""
Implements the various matplotlib plots for this project.
"""
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
import pandas as pd
from IPython import display
import matplotlib.patches as patches

from model import Environment
from roles import Unassigned, Follower, Leader, Pheromone


def plot_p_fl(df):
    """
    Creates (and shows) the p vs (f + l) plot.

    Args:
        df: the dataframe containing 'pheromone', 'followers', and 'leaders'
    """
    plt.figure()
    plt.scatter(df['pheromone'], df['followers'] + df['leaders'])
    plt.xlabel(r'$p$')
    plt.ylabel(r'$f + l$')
    plt.show()


def plot_col(ax, df, cols):
    """
    Plots the variables in the cols list.

    Args:
        df: the dataframe containing entries from cols
        cols: list containing the dict entries to be plotted.
    """
    plt.figure()
    df[cols].plot()
    plt.show()


def plot_continuous(env, steps=1000):
    """
    Shows the passed environment over time. Terminates gracefully when closing
    the animation window.

    Args:
        env: the environment to be shown
        steps (int): the amount of steps to animate (default 1000)
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim([0, env.width])
    ax.set_ylim([0, env.height])
    env.animate(ax)
    fig_num = plt.get_fignums()[0]
    custom_patches = [
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='g', fill=True, zorder=2),
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='r', fill=True, zorder=2),
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='b', fill=True, zorder=2),
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='c', fill=True, zorder=2)]
    ax.legend(custom_patches, ['Unassigned', 'Follower', 'Leader', 'Pheromoner'], loc='center left',
              bbox_to_anchor=(1, 0.5))
    for i in range(steps):
        if not plt.fignum_exists(fig_num): break

        plt.title('iteration: ' + str(i))
        plt.pause(0.001)

        # Take a step
        env.step()

        # Store the state for animation
        env.animate(ax)
        fig.canvas.draw()


def plot_continuous_notebook(env, steps=1000):
    """
    Shows the passed environment over time. Terminates gracefully when closing
    the animation window. Notebook version, meaning that it clears the display
    before showing the next animation frame.

    Args:
        env: the environment to be shown
        steps (int): the amount of steps to animate (default 1000)
    """

    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.set_xlim([0, env.width])
    ax1.set_ylim([0, env.height])
    ax2.set_ylabel('number of ants')
    env.animate(ax1)
    fig_num = plt.get_fignums()[0]
    custom_patches = [
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='g', fill=True, zorder=2),
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='r', fill=True, zorder=2),
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='b', fill=True, zorder=2),
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='c', fill=True, zorder=2)]
    ax1.legend(custom_patches, ['Unassigned', 'Follower', 'Leader', 'Pheromoner'], loc='center right',
               bbox_to_anchor=(0, 0.5))

    # Flush display
    display.clear_output(wait=True)
    display.display(plt.gcf())

    for i in range(steps):
        if not plt.fignum_exists(fig_num): break

        plt.suptitle('iteration: ' + str(i))
        ax2.set_ylabel('number of ants')
        ax2.set_ylim([-0.1, env.N])
        plt.pause(0.001)

        # Take a step
        env.step()

        # Store the state for animation
        env.animate(ax1)
        env.dc.get_model_vars_dataframe()[['leaders', 'unassigned', 'followers', 'pheromone']].plot(ax=ax2, legend=None,
                                                                                                    color=['b', 'g',
                                                                                                           'r', 'c'])

        fig.canvas.draw()

        # Flush display
        display.clear_output(wait=True)
        display.display(plt.gcf())
        ax2.clear()
    plt.show()


def plot_param_var(ax, df, param, var):
    """
    Helper function for plot_all_vars. Plots the individual parameter vs
    variables passed.

    Args:
        ax: the axis to plot to
        df: dataframe that holds the data to be plotted
        param: parametersto be taken from the dataframe
        var: which output variable to plot
    """
    x = df.groupby(param).mean().reset_index()[param]
    y = df.groupby(param).mean()[var]
    replicates = df.groupby(param)[var].count()
    err = (1.96 * df.groupby(param)[var].std()) / np.sqrt(replicates)
    ax.errorbar(x, y, yerr=err.as_matrix())

    ax.scatter(df[param], df[var])
    ax.set_xlabel(param)
    ax.set_ylabel(var)
    ax.set_ylim([-1.1, 1.1])


def plot_param_var_conf(ax, df, param, var, label='_nolegend_', alpha=1, line_to_legend=False):
    """
    Helper function for plot_all_vars. Plots the individual parameter vs
    variables passed.

    Args:
        ax: the axis to plot to
        df: dataframe that holds the data to be plotted
        param: parametersto be taken from the dataframe
        var: which output variable to plot
    """
    x = df.groupby(param).mean().reset_index()[param]
    y = df.groupby(param).mean()[var]
    replicates = df.groupby(param)[var].count()
    err = (1.96 * df.groupby(param)[var].std()) / np.sqrt(replicates)
    ax.plot(x, y, c='k', label='_nolegend_')
    ax.fill_between(x, y - err, y + err, label=label, alpha=alpha)

    ax.set_xlabel(param)
    ax.set_ylabel(var)
    ax.set_ylim([-1.1, 1.1])


def plot_all_vars(df, param):
    """
    Plots the parameters passed vs each of the output variables.

    Args:
        df: dataframe that holds all data
        param: the parameter to be plotted
    """

    f, axs = plt.subplots(3, figsize=(7, 10))
    plot_param_var(axs[0], df, param, 'pfl_net')
    plot_param_var(axs[1], df, param, 'pu_net')
    plot_param_var(axs[2], df, param, 'flu_net')


def plot_index(s, params, i, title=''):
    """
    Creates a plot for Sobol sensitivity analysis that shows the contributions
    of each parameter to the global sensitivity.

    Args:
        s (dict): dictionary {'S#': dict, 'S#_conf': dict} of dicts that hold
            the values for a set of parameters
        params (list): the parameters taken from s
        i (str): string that indicates what order the sensitivity is.
        title (str): title for the plot
    """

    if i == '2':
        p = len(params)
        params = list(combinations(params, 2))
        indices = s['S' + i].reshape((p ** 2))
        indices = indices[~np.isnan(indices)]
        errors = s['S' + i + '_conf'].reshape((p ** 2))
        errors = errors[~np.isnan(errors)]
        plt.figure(figsize=(10,6))
    else:
        indices = s['S' + i]
        errors = s['S' + i + '_conf']
        plt.figure()

    l = len(indices)

    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')
