# -*- coding: utf-8 -*-
"""
Roles module. These objects can be used to specify roles for agents.

Note:
    - When implementing new 'roles' keep in mind that 'self' is actually the Ant
    agent that was passed when calling the method.
    - With 'Pheromone' an ant is meant with a pheromone role. Not the chemical itself.

Core Objects:
    Role: Base class. Raises NotImplementedError if methods are not overloaded.
    Unassigned: Has no current role. When meeting a Leader, has a chance to
        become a follower of that leader. When meeting a Pheromone, has a chance
        to become a Pheromone.
    Follower: Follows a leader. Has no special actions.
    Leader: Leads a group of followers. When finding one of it's own followers,
        will have a chance to change all followers into leaders. When finding
        anyone else, has a chance to change all followers and itself into
        unassigned.
    Pheromone: Pheromone only has a chance to stop being a pheromone when
        meeting anyone but another pheromone.
"""
import random
import numpy as np

class Role:
    """ Base class for roles. Use as super to implement new roles. """
    def get_visualization_color():
        """ The colorstring for matplotlib goes here. """
        raise NotImplementedError

    def role_actions(self):
        """ The role's actions go here. """
        raise NotImplementedError

class Unassigned(Role):
    """
    Has no current role. When meeting a Leader, has a chance to become a
    follower of that leader. When meeting a Pheromone, has a chance to become a
    Pheromone.
    """
    def get_visualization_color():
        """
        Returns:
            The colorstring 'green' for matplotlib.
        """
        return 'g'

    def role_actions(self):
        """
        Applies the actions that should be done every step for an agent with the
        'Unassigned' role.

        Can either change to a follower or a pheromone when meeting a leader or
        a pheromone respectively.

        Note:
            'self' is an Ant agent object here.
        """
        neighbors = self.get_neighbors()

        if neighbors:
            n = random.choice(list(neighbors))

            transition_chance, new_role = self.model.interaction_probs[n.role]

            if np.random.random() < transition_chance:
                # If the leader is not yet full
                if n.role == Leader and len(n.followers) < self.model.max_group_size:
                    n.followers.append(self)
                    self.role = new_role
                elif n.role == Pheromone:
                    self.role = new_role

class Follower(Role):
    """ Follows a leader. Has no special actions. """
    def get_visualization_color():
        """
        Returns:
            The colorstring 'red' for matplotlib.
        """
        return 'r'

    def role_actions(self):
        """ Followers have no role-specific actions. """
        pass

class Leader(Role):
    """
    Leads a group of followers. When finding one of it's own followers, will
    have a chance to change all followers into leaders. When finding anyone
    else, has a chance to change all followers and itself into unassigned.
    """
    def get_visualization_color():
        """
        Returns:
            The colorstring 'blue' for matplotlib.
        """
        return 'b'

    def role_actions(self):
        """
        Applies the actions that should be done every step for an agent with the
        'Leader' role.

        When meeting one of it's followers, has a chance to succeed, and make
        each of it's followers a leader.

        When meeting anything else, has a chance to fail, and make each of it's
        followers and itself unassigned.

        Note:
            'self' is an Ant agent object here.
        """
        neighbors = self.get_neighbors()

        if neighbors:
            n = random.choice(list(neighbors))

            if n in self.followers:
                transition_chance, new_role = self.model.interaction_probs["success"]
            else:
                transition_chance, new_role = self.model.interaction_probs["failure"]

            # Apply transition to each of the followers.
            if np.random.random() < transition_chance:
                for follower in self.followers:
                    follower.role = new_role

                self.role = new_role
                self.followers = []

class Pheromone(Role):
    """
    Pheromone only has a chance to stop being a pheromone when meeting anyone
    but another pheromone.
    """
    def get_visualization_color():
        """
        Returns:
            The colorstring 'cyan' for matplotlib.
        """
        return 'c'

    def role_actions(self):
        """
        Applies the actions that should be done every step for an agent with the
        'Pheromone' role.

        When meeting anything but it's own role, will have a chance to become
        unassigned.

        Note:
            'self' is an Ant agent object here.
        """
        neighbors = self.get_neighbors()

        if neighbors:
            n = random.choice(list(neighbors))
            if n.role != self.role:
                event_chance, new_role = self.model.interaction_probs["scent_lost"]
                if np.random.random() < event_chance:
                    self.role = new_role
