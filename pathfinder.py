import pygame
from pygame.locals import *
import sys
import random

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
WINDOW_SIZE = (600,600)
WIDTH = 50
HEIGHT = 50

MARGIN = 10
grid = []
grid = [[0 for x in range(10)] for y in range(10)]
button_down = False
last_row = 0
last_column = 0

class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]

    def printSolution(self, dist):
        print("Vertex \tDistance from Source")
        print(dist)
        for node in range(self.V):
            print(node, "\t", dist[node])

    def minDistance(self, dist,sptSet):
        min_index = 0
        min = 1000000000
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
        return min_index

    def dijkstra(self, src):
        dist = [1000000000] * self.V
        dist[src] = 0
        sptSet = [False] * self.V

        for cout in range(self.V):
            u = self.minDistance(dist, sptSet)

            sptSet[u] = True

            for v in range(self.V):
                print("Currently testing: " ,u,v)
                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
        self.printSolution(dist)

if __name__ == "__main__":
    print("Hello world")
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Hello World")
    goal_x = random.randint(0,10)
    goal_y = random.randint(0,10)
    start_x = random.randint(0,10)
    start_y = random.randint(0,10)
    g = Graph(10)
    print(goal_x, goal_y, start_x, start_y)
    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                button_down = False
            elif event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_RETURN):
                    print("Running algorithm ")
                    g.graph = grid
                    g.dijkstra(0)
            if(button_down):
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                print("Click ", pos, "Grid coordinates: ", row, column)
                if(last_row != row or last_column != column):
                    if (grid[row][column] == 0):
                        if(row == goal_x and goal_y == column):
                            grid[row][column] = 0
                        elif(row == start_x and column == start_y):
                            grid[row][column] = 0
                        else:
                            grid[row][column] = 1
                    else:
                        grid[row][column] = 0
                last_row = row
                last_column = column
        DISPLAYSURF.fill(BLACK)

        for row in range(10):
            for column in range(10):
                color = WHITE
                if grid[row][column] == 1:
                    color = GREEN
                elif row == goal_x and goal_y == column:
                    pygame.draw.rect(DISPLAYSURF, GREEN, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
                elif row == start_x and start_y == column:
                    pygame.draw.rect(DISPLAYSURF, RED, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
                else:
                    pygame.draw.rect(DISPLAYSURF, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
        pygame.display.update()
