from mesa import Agent
import numpy as np
import matplotlib.patches as patches

class Obstacle(Agent):
    """An obstacle kind of agent."""

    def __init__(self, environment, pos=None, cost=-1):
        self.environment = environment
        self.passable = None        # passable set by assigning a cost
        self.cost = cost
        self._patch = None

        # make sure that obstacle can't be at same place as food or colony
        # TODO: obstacle should not be placed on colony or obstacle itself
        if pos == None:
            pos = self.environment.get_random_position()

            while(self.environment.position_taken(pos)):
                pos = self.environment.get_random_position()

        self.pos = pos

        # register self
        self.environment.grid.place_agent(self, self.pos)

    def on_obstacle(self, pos):
        return pos == self.pos

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, new_cost):
        self._cost = new_cost
        self.passable = new_cost >= 0

    def update_vis(self):
        radius = 0.4
        if not self._patch:
            self._patch = patches.Circle(self.environment.grid_to_array(self.pos), radius, linewidth=2,
                                         edgecolor='y', facecolor='y', fill=True, zorder=1)
            self.environment.ax.add_patch(self._patch)
        else:
            pos = self.environment.grid_to_array((self.pos[0] + 0.5, self.pos[1] - 0.5))
            self._patch.center = pos

        return self._patch