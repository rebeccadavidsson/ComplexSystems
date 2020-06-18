from model import Environment
from plot import plot_continuous_notebook
import matplotlib.pyplot as plt


# Create the environment for 10 ants
steps = 100
env = Environment(N=15, g=1, size=20, p_uf=0.5, p_pu=0.1, p_up=0.5, p_fl=0.8, p_lu=0.05,
    ratio=0.2, moore=False, grow=False)
# Use the continuous plot function from plot.py to animate the model
# plt.xkcd()
plot_continuous_notebook(env, steps)
