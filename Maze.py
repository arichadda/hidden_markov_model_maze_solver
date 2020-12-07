# Ari Chadda
# PA6 CS76 - 11/10/20

import random


class Maze:
    # generally the same maze code from PA2 with a few additions for this problem
    def __init__(self, mazefilename):

        self.robotloc = []
        f = open(mazefilename)
        lines = [] # open and read the file line by line
        for line in f:
            line = line.strip()
            if len(line) == 0:
                pass
            elif line[0] == "\\": # the \ denotes the location the robot starts at in the file
                parms = line.split()
                x = int(parms[1])
                y = int(parms[2])
                self.robotloc.append(x) # add the robot locaiotn
                self.robotloc.append(y)
            else:
                lines.append(line)
        f.close()

        self.width = len(lines[0]) # maze dimensions
        self.height = len(lines)
        self.color_options = ["r", "g", "y", "b"] # color options

        self.map = list("".join(lines))

    def index(self, x, y):
        return (self.height - y - 1) * self.width + x

    def is_floor(self, x, y): # check if valid floor
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        if self.map[self.index(x, y)] == "r" or self.map[self.index(x, y)] == "g" or self.map[self.index(x, y)] == "b" \
                or self.map[self.index(x, y)] == "y": # if it is colored one of the colors, it is a floor
            return True
        return False

    def get_points(self):
        locations = {} # dictionary for all the points in the maze

        for x in range(self.width):
            for y in range(self.height):
                if self.map[self.index(x, y)]:
                    locations[(x, y)] = self.map[self.index(x, y)] # add the points as keys
        return locations # value will be probability

    def get_walls(self):
        walls = [] # list of walls

        for x in range(self.width):
            for y in range(self.height):
                if self.map[self.index(x, y)] == "#": # if wall character in maze list
                    walls.append((x, y)) # add it to the walls list
        return walls # return the locaiton of the walls

    def get_color(self, x, y): # gets the color of the tile
        probability = random.random()

        if probability < 0.88: # correct reading 88% of the time
            return self.map[self.index(x, y)]
        else: # otherwise evenly distributed random color from the options
            return random.choice(self.color_options)

    def create_render_list(self): # creating the list for printing
        renderlist = list(self.map)

        robot_number = 0
        for index in range(0, len(self.robotloc), 2):

            x = self.robotloc[index] # adding the robot location to the list
            y = self.robotloc[index + 1]

            renderlist[self.index(x, y)] = robotchar(robot_number)
            robot_number += 1

        return renderlist



    def __str__(self): # for printing the maze
        renderlist = self.create_render_list()

        s = ""
        for y in range(self.height - 1, -1, -1): # creates string by looping through list
            for x in range(self.width):
                s += renderlist[self.index(x, y)] # concatenting the maze

            s += "\n" # adding new line after every row

        return s


def robotchar(robot_number): # the robot on the maze will have the letter A
    return chr(ord("A") + robot_number)


if __name__ == "__main__": # some maze testing code
    test_maze1 = Maze("maze1.maz")
    print(test_maze1)

    print(test_maze1.robotloc)

    print(test_maze1.is_floor(2, 3))
    print(test_maze1.is_floor(-1, 3))
    print(test_maze1.is_floor(1, 0))
    print(test_maze1.get_color(3, 0))

    print(len(test_maze1.get_points()))


