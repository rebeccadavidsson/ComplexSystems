# -*- coding: utf-8 -*-
"""
The Ant class implements the ant's properties and updates.

Core Objects:
    Ant: Extends the Agent class from Mesa.
"""
import numpy as np
import random
import matplotlib.patches as patches

from mesa import Agent

from roles import Unassigned, Follower, Leader, Pheromone
from copy import copy

class Ant(Agent):
    """ Model agent Ant."""

    def __init__(self, id, model, pos=None, role=Unassigned):
        """
        Args:
            id (int): a unique id to represent the agent
            model (Model): the model to link the agent to
            pos (tuple): the position to start the ant on (int x, int y)
        """
        super(Ant, self).__init__(id, model)

        # Agent attributes
        self.model = model

        self._role = None
        self.role = role

        # Agent variables
        self.pos = pos if pos is not None else self.model.get_random_position()

        self.followers = []

        # Visualization
        self._patch = None
        self.size = 0.4

    @property
    def role(self):
        """ Returns the current role of the ant. """
        return self._role

    @role.setter
    def role(self, new_role):
        """
        Sets the new role for the ant.

        Args:
            new_role (Role): class that defines the action set of the ant
        """
        self._role = new_role

    def get_neighbors(self):
        """
        Get the neighbors of the ant at it's current position.

        Returns:
            A set of neighbors.
        """
        x, y = self.pos

        neighbors = copy(self.model.grid.grid[x][y])

        neighbors.remove(self)

        return neighbors

    def step(self):
        """ Steps the ant one timestep. First move, then do actions. """
        self.move()

        self.role.role_actions(self)

    def move(self):
        """
        Moves the ant randomly (random walk). Each of the possible directions
        can be chosen with an equal probability.
        """
        possibilities = list(self.model.get_torus_neighborhood(self.pos, self.model.moore))

        self.model.move_agent(self, random.choice(possibilities))

    def update_vis(self):
        """
        Updates the ant's patch in the visualization.

        Returns:
            The patch that corresponds to this ant.
        """
        pos = self.model.grid_to_array(self.pos)
        pos = (pos[0] + (1 - self.size) / 2, pos[1] + (1 - self.size) / 2)

        if not self._patch:
            self._patch = patches.Rectangle(pos, self.size, self.size, linewidth=2,
                                            edgecolor='k', facecolor='w', fill=True, zorder=2)
            self.model.ax.add_patch(self._patch)

        self._patch.set_facecolor(self.role.get_visualization_color())
        self._patch.set_xy(pos)

        return self._patch
