import numpy as np
import matplotlib.patches as patches


class FoodGrid:
    """ Class that keeps track of where food is in its own grid. """
    def __init__(self, environment):
        self.environment = environment
        self.width = environment.width
        self.height = environment.height
        self.grid = np.zeros((self.width, self.height))

        # animation attributes
        self._patches = []

    def step(self):
        """
        When there is no more food left on the map, add one food location.
        """
        # if len(np.where(self.grid > 0)[0]) == 0:
        #     self.add_food()

    def add_food(self, xy=None):
        """
        Adds food on the position specified by xy. If no xy is specified a random location is seleced that is not on a
        colony.
        :param xy: a tuple of integers (x, y)
        """

        # for i in range(0,4):
            # while not xy:
            #     x = np.random.randint(0, self.width, 1)[0]
            #     y = np.random.randint(0, self.height, 1)[0]
            #
            #     if not any([colony.on_colony((x, y)) for colony in self.environment.colonies]):
            #         xy = (x, y)
        # self.grid[xy] += 50
        # xy=None
        locations = [(5, 5), (20, 5), (14, 24)]
        for location in locations:
            xy = (location[0], location[1])
            self.grid[xy] += 50

    def get_food_pos(self):
        """
        Returns a list of tuples of all the x, y positions
        :return: [(x, y), (x, y), ...]
        """
        return [(x, y) for x, y in np.array(np.where(self.grid > 0)).T.tolist()]

    def update_vis(self):
        """

        :return:
        """
        food_spots = [self.environment.grid_to_array(pos) for pos in self.get_food_pos()]

        for i in range(max([len(food_spots), len(self._patches)])):
            if i > len(self._patches) - 1:
                patch = patches.Rectangle(self.environment.grid_to_array(food_spots[i]), 1, 1, linewidth=1, edgecolor='g',
                                          facecolor='g', fill=True, zorder=1)
                self._patches.append(patch)
                self.environment.ax.add_patch(patch)
            elif i > len(food_spots) - 1:
                self._patches[i].remove()
                self._patches.pop(i)
            else:
                self._patches[i].set_xy(food_spots[i])

        return self._patches

    def __exit__(self):
        """
        Make sure the animation is update accordingly to the removed food
        """
        raise NotImplementedError
