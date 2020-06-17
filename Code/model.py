# -*- coding: utf-8 -*-
"""
The Environment class implements the Environment's properties and updates.

Core Objects:
    Environment: Extends the Model class from Mesa.
"""
import numpy as np

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from ant import Ant
from roles import Unassigned, Follower, Leader, Pheromone

class Environment(Model):
    """ A model which contains ants with specified roles. """

    def __init__(self, N=10, g=1, size=10, p_uf=0.5, p_pu=0.1, p_up=0.5, p_fl=0.8, p_lu=0.05,
                 ratio=0.5, moore=False, grow=False):
        """
        Args:
            N (int): number of ants
            g (float): the max group size of an Ant relative to N
            size(int): the size of the system (size X size)
            p_uf (float): the probability that Unassigned changes to Follower
            p_pu (float): the probability that Pheromone changes to Unassigned
            p_up (float): the probability that Unassigned changes to Pheromone
            p_fl (float): the probability that Follower changes to Leader
            p_lu (float): the probability that Leader changes to Unassigned
            ratio (float): the start ratio of leaders (1 - ratio is the start nr of pheromone)
            moore (bool): True/False whether Moore/vonNeumann is used
            grow (bool): True/False whether the system grows over time or not
        """
        super().__init__()

        # Environment variables
        size = int(size)
        self.width = size
        self.height = size
        self.moore = moore
        self.grow = grow
        self.grid = MultiGrid(size, size, torus=True)
        self.interaction_probs = {Unassigned: (-1, None),
                                  Follower: (-1, None),
                                  Leader: (p_uf, Follower),
                                  Pheromone: (p_up, Pheromone),
                                  "success": (p_fl, Leader),
                                  "failure": (p_lu, Unassigned),
                                  "scent_lost": (p_pu, Unassigned)}
        self.ant_counter = 0

        # Environment attributes
        self.schedule = RandomActivation(self)

        # Ant variables
        N = int(N)
        self.N = N
        self.g = g
        self.max_group_size = np.round(g * N) if np.round(g * N) >= 1 else 1
        role_division = {Unassigned: np.round(N//2),
                         Follower: 0,
                         Leader: int((N//2)*ratio),
                         Pheromone: N - np.round(N//2) - int((N//2)*ratio)}
        self.role_division = role_division

        for role, number in role_division.items():
            self.add_ants(number, role)

        model_reporters = {"unassigned": lambda m: sum([1 if a.role == Unassigned else 0 for a in m.schedule.agents]),
                           "followers": lambda m: sum([1 if a.role == Follower else 0 for a in m.schedule.agents]),
                           "leaders": lambda m: sum([1 if a.role == Leader else 0 for a in m.schedule.agents]),
                           "pheromone": lambda m: sum([1 if a.role == Pheromone else 0 for a in m.schedule.agents])}
        self.dc = DataCollector(model_reporters=model_reporters)

    def get_torus_coordinates(self, x, y):
        """
        Gives correct coordinates if the coordinates are out of bounds.

        Args:
            x (int): current x position
            y (int): current y position

        Returns:
            Tuple of (x, y) that is in ([0, width], [0, height])
        """
        return x % self.width, y % self.height

    def get_torus_neighborhood(self, pos, moore, radius=1, include_center=False):
        """
        Faster alternative to the mesa built-in grid.get_neighbourhood().

        Args:
            pos (tuple): tuple of position (int x, int y)
            moore (bool): if True, uses Moore's neighborhood
                   if False, uses Neumann's neighborhood
            radius (int): decides the radius of the neighborhood (default 1)
            include_center (bool): if True, include the center
                            if False, do not include the center
                            (default False)

        Returns:
            An iterator that gives all coordinates that are connected to pos
            through the given neighborhood
        """
        x, y = pos

        coordinates = set()

        # Loop over Moore's neighborhood
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx == 0 and dy == 0 and not include_center:
                    continue

                # Skip anything outside the manhattan distance for Neumann
                if not moore and abs(dx) + abs(dy) > radius:
                    continue

                px, py = x + dx, y + dy

                px, py = self.get_torus_coordinates(px, py)

                coords = (px, py)

                if coords not in coordinates:
                    coordinates.add(coords)
                    yield coords

    def get_random_position(self):
        """
        Gets a random position in the grid, samples from a uniform distribution.

        Returns:
            Tuple position (int x, int y)
        """
        return (np.random.randint(0, self.width), np.random.randint(0, self.height))

    def add_ants(self, N, role):
        """
        Adds N ants of with role role to this colony.

        Args:
            N (int): integer value which specifies the nr of ants to add
            role (Role): one of {Unassigned, Follower, Leader, Pheromone}
        """

        for _ in range(N):
            a = Ant(self.ant_counter, model=self, pos=None, role=role)

            self.grid.place_agent(a, a.pos)
            self.schedule.add(a)

            self.ant_counter += 1

    def move_agent(self, ant, pos):
        """
        Move an agent across the map.

        Args:
            ant (Ant): what agent to move
            pos (tuple): (int x, int y) to move the agent to
        """
        self.grid.move_agent(ant, pos)

    def step(self):
        """
        Do a single time-step using freeze-dry states, colonies are updated each time-step in random orders, and ants
        are updated per colony in random order.
        """
        self.schedule.step()
        self.dc.collect(self)

        if self.grow:
            self.add_ants(1, Unassigned)
            self.N += 1


    def animate(self, ax):
        """
        Update the visualization part of the Ants.

        Args:
            ax (Axes): axes binding of matplotlib to animate on
        """
        self.ax = ax
        self.animate_ants()

    def animate_ants(self):
        """ Ask the ants to update themselfs in the animation. """
        for ant in self.schedule.agents:
            ant.update_vis()

    def grid_to_array(self, pos):
        """
        Convert the position/indices on self.grid to imshow array.

        Args:
            pos (tuple): (int x, int y)
        Returns:
            tuple (int: x, int: y), that contains the converted position
        """
        return pos[0], self.height - pos[1] - 1
