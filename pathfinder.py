import pygame
from pygame.locals import *
import sys
import random
import math


class Pathfinder:
    def __init__(self):
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.GREEN = (0,255,0)
        self.RED = (255,0,0)
        self.ORANGE = (255,165,0)
        self.BLUE = (0,0,255)
        self.WINDOW_SIZE = (600,600)
        self.GRAPH_SIZE = 50
        self.WIDTH = 10
        self.found_solution = False
        self.HEIGHT = 10
        self.distances = {}
        self.previous = {}
        self.Q = []
        self.MARGIN = self.WIDTH/5
        self.grid = []
        self.grid = [[0 for x in range(self.GRAPH_SIZE)] for y in range(self.GRAPH_SIZE)]
        self.button_down = False
        self.last_row = 0
        self.last_column = 0
        self.goal_x = random.randint(0,self.GRAPH_SIZE-1)
        self.goal_y = random.randint(0,self.GRAPH_SIZE-1)
        self.start_x = random.randint(0,self.GRAPH_SIZE-1)
        self.start_y = random.randint(0,self.GRAPH_SIZE-1)
        self.DISPLAYSURF = pygame.display.set_mode(self.WINDOW_SIZE)
        self.run_algo = False
        self.counter = 0
        self.path = []
        pygame.init()
        pygame.display.set_caption("Hello World")
    def draw(self):
        self.DISPLAYSURF.fill(self.BLACK)
        for row in range(self.GRAPH_SIZE):
            for column in range(self.GRAPH_SIZE):
                color = self.WHITE
                if self.grid[row][column] == 1:
                    color = self.BLACK
                    pygame.draw.rect(self.DISPLAYSURF, color, [(self.MARGIN + self.WIDTH) * column + self.MARGIN, (self.MARGIN + self.HEIGHT) * row + self.MARGIN, self.WIDTH, self.HEIGHT])
                elif row == self.goal_x and self.goal_y == column:
                    pygame.draw.rect(self.DISPLAYSURF, self.RED, [(self.MARGIN + self.WIDTH) * column + self.MARGIN, (self.MARGIN + self.HEIGHT) * row + self.MARGIN, self.WIDTH, self.HEIGHT])
                elif row == self.start_x and self.start_y == column:
                    pygame.draw.rect(self.DISPLAYSURF, self.GREEN, [(self.MARGIN + self.WIDTH) * column + self.MARGIN, (self.MARGIN + self.HEIGHT) * row + self.MARGIN, self.WIDTH, self.HEIGHT])
                elif self.grid[row][column] == 5:
                    color = self.ORANGE
                    pygame.draw.rect(self.DISPLAYSURF, color, [(self.MARGIN + self.WIDTH) * column + self.MARGIN, (self.MARGIN + self.HEIGHT) * row + self.MARGIN, self.WIDTH, self.HEIGHT])
                elif self.grid[row][column] == 3:
                    color = self.BLUE
                    pygame.draw.rect(self.DISPLAYSURF, color, [(self.MARGIN + self.WIDTH) * column + self.MARGIN, (self.MARGIN + self.HEIGHT) * row + self.MARGIN, self.WIDTH, self.HEIGHT])
                else:
                    pygame.draw.rect(self.DISPLAYSURF, color, [(self.MARGIN + self.WIDTH) * column + self.MARGIN, (self.MARGIN + self.HEIGHT) * row + self.MARGIN, self.WIDTH, self.HEIGHT])
        pygame.display.update()
    def get_neighbors(self, point):
        neighbors = []
        if point[0] + 1 <= self.GRAPH_SIZE:
            neighbors.append((point[0] + 1, point[1]))
        if point[0] - 1 >= 0:
            neighbors.append((point[0] -1, point[1]))
        if point[1] + 1 <= self.GRAPH_SIZE:
            neighbors.append((point[0] ,point[1] + 1))
        if point[1] -1 >= 0:
            neighbors.append((point[0], point[1] - 1))

        return neighbors
    def get_dist(self, point, U):

        if self.grid[point[0]][point[1]] == 1:
            return 2**100
        return math.sqrt( ((U[0] - point[0])**2 + (U[1] - point[1])**2) )
    def set_path(self, path):
        for point in path:
            self.grid[point[0]][point[1]] = 5
    def init_dijkstra(self):
        for row in range(self.GRAPH_SIZE):
            for column in range(self.GRAPH_SIZE):
                self.distances[(row,column)] = 2**100
                self.previous[(row,column)] = None
                self.Q.append((row,column))
        self.distances[(self.start_x, self.start_y)] = 0

    def get_smallest_in_q(self):
        smallest_val = 2**1000
        smallest_point = ""
        for point in self.Q:
            if self.distances[point] < smallest_val:
                smallest_val = self.distances[point]
                smallest_point = point
        return smallest_point

    def get_path(self):
        path = []
        path.append((self.goal_x, self.goal_y))
        next_val = (self.goal_x, self.goal_y)
        while True:
            next_val = self.previous[next_val]
            path.append(next_val)
            if next_val == (self.start_x, self.start_y):
                return path
    def reset(self):
        self.grid = [[0 for x in range(self.GRAPH_SIZE)] for y in range(self.GRAPH_SIZE)]
        self.goal_x = random.randint(0,self.GRAPH_SIZE-1)
        self.goal_y = random.randint(0,self.GRAPH_SIZE-1)
        self.start_x = random.randint(0,self.GRAPH_SIZE-1)
        self.start_y = random.randint(0,self.GRAPH_SIZE-1)
        self.found_solution = False
        self.run_algo = False
        self.button_down = False
        self.last_row = 0
        self.last_column = 0
        self.path = []
        self.counter = 0
        self.init_dijkstra()
    def run_game(self):
        print(self.goal_x, self.goal_y, self.start_x, self.start_y)
        self.init_dijkstra()
        while True:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.button_down = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.button_down = False
                elif event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_RETURN):
                        print("Running algo")
                        self.run_algo = True
                    if(event.key == pygame.K_BACKSPACE):
                        print("RESETING")
                        self.reset()
                if(self.button_down):
                    column = int(pos[0] // (self.WIDTH + self.MARGIN))
                    row = int(pos[1] // (self.HEIGHT + self.MARGIN))
                    print("Click ", pos, "Grid coordinates: ", row, column)
                    if(self.last_row != row or self.last_column != column):
                        if (self.grid[row][column] == 0):
                            if(row == self.goal_x and self.goal_y == column):
                                self.grid[row][column] = 0
                            elif(row == self.start_x and column == self.start_y):
                                self.grid[row][column] = 0
                            else:
                                self.grid[row][column] = 1
                        else:
                            self.grid[row][column] = 0
                    self.last_row = row
                    self.last_column = column
            if(self.run_algo):

                if len(self.Q) > 0 and self.found_solution == False:
                    U = self.get_smallest_in_q()
                    self.Q.remove(U)
                    neighbors = self.get_neighbors(U)
                    for neighbor in neighbors:
                        if neighbor in self.Q:
                            if self.grid[neighbor[0]][neighbor[1]] == 0:
                                self.grid[neighbor[0]][neighbor[1]] = 3
                                alt = self.distances[U] + self.get_dist(neighbor, U)
                                if alt < self.distances[neighbor]:
                                    self.distances[neighbor] = alt
                                    self.previous[neighbor] = U
                                if neighbor == (self.goal_x, self.goal_y):
                                    self.found_solution = True
                if self.found_solution:

                    try:
                        self.path = self.get_path()
                        if self.counter < len(self.path):
                            current_point = self.path[self.counter]
                            self.grid[current_point[0]][current_point[1]] = 5
                            self.counter += 1
                    except Exception as e:
                        print("No solution!")
                        self.run_algo = False
            self.draw()

if __name__ == "__main__":
    print("Hello world")



    p = Pathfinder()
    p.run_game()
