# Ari Chadda
# PA6 CS76 - 11/10/20

import random
import numpy as np

class HiddenMarkovModel:

    def __init__(self, maze):
        self.maze = maze # maze object
        self.current_x = maze.robotloc[0]
        self.current_y = maze.robotloc[1]
        self.max_iterations = 5 # max number of iterations
        # may want to increase

        self.points = maze.get_points() # all the points in the maze
        self.maze_walls = maze.get_walls() # wall coordinates

        self.particles = {} # points and probabilities

        self.move_sequence = [] # ground truth moves
        self.color_sequence = [] # recorded color and direction
        self.map_list = [] # list of the maze
        self.accessible = [] # the coordinates accessible from the hypothesized location

        self.prior_matrix = None # matricies for filter formula
        self.current_matrix = None
        self.predict_matrix = None

    def particle_filtering(self):
        self.move_sequence, self.color_sequence = self.move_robot() # get ground truth as well as readings

        self.particles = self.initalize_weights() # add prior weights to dictionary
        prior_list = list(self.particles.values())

        prior = []
        sub_list = []
        for element in prior_list: # convert the list to a matrix
            sub_list.append(element)
            if len(sub_list) == 4:
                prior.append(sub_list)
                sub_list = []
        self.prior_matrix = np.array(prior)
        self.prior_matrix = np.rot90(self.prior_matrix) # first prior matrix

        self.create_map() # create the maze map list

        for color in range(len(self.color_sequence)): # steps of the filtering algorithm
            self.predict()
            self.predict_matrix = self.update(self.color_sequence[color])
            self.normalize_weights()
            self.display_weights(color)

    def predict(self): # prediction based on movement model
        for point in self.accessible: # if accessible square from move

            if self.maze.is_floor(point[0], point[1]): # robot can move one way in each direction
                self.particles[(point[0], point[1])] = 0.25 # if free square has a .25 option

            count = 0 # if a side is blocked then the robot has a chance of staying on the same square
            if not self.maze.is_floor(point[0] + 1, point[1]):
                count += 0.25
            if not self.maze.is_floor(point[0] - 1, point[1]):
                count += 0.25
            if not self.maze.is_floor(point[0], point[1] + 1):
                count += 0.25
            if not self.maze.is_floor(point[0], point[1] - 1):
                count += 0.25

            if count > 0: # chance of staying on the same square increases with number of closed sides
                self.particles[point] = count
        self.accessible = [] # reset accessible list

    def update(self, color):
        possibilities = [] # update prediction based upon sensor model
        count = -1
        for row in self.map_list:
            count += 1 # get the color
            if color[1] in row:
                idx = -1
                for point in row:
                    idx += 1
                    if color[1] == point:
                        possibilities.append((idx, count)) # get the possible squares with the same color

        for option in possibilities: # create the accessible list for prediction
            if self.maze.is_floor(option[0] + 1, option[1]):
                self.accessible.append((option[0] + 1, option[1]))
            if self.maze.is_floor(option[0] - 1, option[1]):
                self.accessible.append((option[0] - 1, option[1]))
            if self.maze.is_floor(option[0], option[1] + 1):
                self.accessible.append((option[0], option[1] + 1))
            if self.maze.is_floor(option[0], option[1] - 1):
                self.accessible.append((option[0], option[1] - 1))
            self.accessible.append((option[0], option[1]))

        if possibilities:
            for key in self.particles.keys():
                if key in possibilities:
                    self.particles[key] *= 0.88 # correct reading chance
                else:
                    self.particles[key] *= 0.04 # incorrect chance
                if key in self.maze_walls:
                    self.particles[key] *= 0 # no chance of being in wall
        current_list = list(self.particles.values())

        current = []
        sub_list = []
        for element in current_list: # create current matrix
            sub_list.append(element)
            if len(sub_list) == 4:
                current.append(sub_list)
                sub_list = []
        self.current_matrix = np.array(current)
        predict = self.current_matrix * self.prior_matrix # multiply matrices elementwise
        predict = np.rot90(predict)


        self.prior_matrix = self.current_matrix
        return predict # return prediction matrix

    def display_weights(self, idx):

        self.maze.robotloc = self.move_sequence[:idx + 1][-1] # iterate through the sequence one at a time

        print("Location sequence: ", self.move_sequence[:idx + 1], '\n')
        print(self.maze)
        predict = np.ndarray.tolist(self.predict_matrix)
        predict = np.array(predict) # print the maze, prediction and ground truth
        print(predict)
        print("------------")

    def move_robot(self):
        moves = [] # creat the move sequence to analyze
        colors = []
        curr_direction = "Start"
        for move in range(self.max_iterations):
            options = ["North", "South", "East", "West"] # can move in one of four directions
            choice = random.choice(options)

            if move == 0:
                moves.append([self.maze.robotloc[0], self.maze.robotloc[1]]) # add the starting location
                colors.append([curr_direction, self.maze.get_color(self.maze.robotloc[0], self.maze.robotloc[1])])

            curr_direction = choice

            if self.maze.is_floor(self.current_x + 1, self.current_y) and choice == "East": # translate move into coords
                self.current_x = self.current_x + 1
            elif self.maze.is_floor(self.current_x - 1, self.current_y) and choice == "West":
                self.current_x = self.current_x - 1
            elif self.maze.is_floor(self.current_x, self.current_y + 1) and choice == "North":
                self.current_y = self.current_y + 1
            elif self.maze.is_floor(self.current_x, self.current_y - 1) and choice == "South":
                self.current_y = self.current_y - 1

            self.maze.robotloc[0] = self.current_x # change the robot locaiton
            self.maze.robotloc[1] = self.current_y

            moves.append([self.maze.robotloc[0], self.maze.robotloc[1]]) # add new location + reading
            colors.append([curr_direction, self.maze.get_color(self.maze.robotloc[0], self.maze.robotloc[1])])

        return moves, colors

    def create_map(self):
        self.maze.robotloc = [] # create the map list in row by row form
        map_list = self.maze.create_render_list()
        sub_list = []
        for point in map_list:

            sub_list.append(point)
            if len(sub_list) == 4:
                self.map_list.append(sub_list)
                sub_list = []
        list.reverse(self.map_list) # reverse for coordinate alignment -- (0,0) in bottom left

    def initalize_weights(self): # initalize weigths - number of empty squares
        return dict.fromkeys(self.points.keys(), 1 / len(self.points))

    def normalize_weights(self):
        total = 0
        for row in self.predict_matrix: # normalieze by creating spread that adds up to 1 or 100% 
            for num in row:
                total += num
        self.predict_matrix = self.predict_matrix / total
        self.predict_matrix = np.round(self.predict_matrix, 3)