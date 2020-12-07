# Ari Chadda
# PA6 CS76 - 11/10/20

from HiddenMarkovModel import HiddenMarkovModel
from Maze import Maze

if __name__ == "__main__":

    # maze options for test
    # test_maze = Maze("maze1.maz")
    test_maze = Maze("maze2.maz")

    maze_solver = HiddenMarkovModel(test_maze) # instantiating solver object
    maze_solver.particle_filtering() # calling filtering algorithm

