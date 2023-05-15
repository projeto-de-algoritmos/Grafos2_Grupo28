import operator
import random
import pygame
from pygame.locals import *
from colorama import Fore, Style
import time

class Maze:
    def __init__(self, lines, columns):
        self.__lines = lines
        self.__columns = columns
        self.__block = '▣'
        self.__freePath = ' '
        self.__minorPath = 'x'
        self.__matrix = self.CreateMatrix()
        self.INFINITY = float('inf')
        self.__dist = dict()
        self.__parent = dict()
        # Using dict comprehension
        # self.__dist = {(element,item): self.INFINITY for element in range(len(matrix)) for item in range(len(matrix[0]))}
        for element in range(self.__lines):
            for item in range(self.__columns):
                self.__dist[(element, item)] = self.INFINITY
                self.__parent[(element, item)] = self.INFINITY

    def Djikstra(self, vStart):
        self.__dist[vStart] = 0
        self.__parent[vStart] = vStart
        quee = [vStart+(0,)]

        while (quee):
            popped = quee.pop(0)[0:2]
            neighbours = self.GetNeighbours(popped[0], popped[1])
            for element in neighbours:
                dist = element[2]+self.__dist[popped]
                if dist < self.__dist[element[0:2]]:
                    quee.append(element)
                    self.__parent[element[0:2]] = popped
                    self.__dist[element[0:2]] = dist
            quee.sort(key=operator.itemgetter(2))

    def DjikstraShotestPath(self, vStart, vEnd):
        self.CreateMaze(vStart)
        self.__matrix[vStart[0]][vStart[1]] = 'A'
        self.__matrix[vEnd[0]][vEnd[1]] = 'B'
        self.Djikstra(vStart)

        if self.__dist[vEnd] != self.INFINITY:
            self.__matrix[vStart[0]][vStart[1]] = self.__minorPath
            shortestPath = [vEnd]
            parent = vEnd
            while parent != vStart:
                self.__matrix[parent[0]][parent[1]] = self.__minorPath
                parent = self.__parent[parent]
                shortestPath.insert(0, parent)

        # Initialize pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        # Set up colors
        BLACK = (0, 0, 0)
        BACKGROUND = (133, 133, 133)
        WALL = (25, 25, 25)
        BLUE = (0, 0, 255)
        PATH = (236, 253, 39)
        GREEN = (0, 255, 0)
        MAGENTA = (255, 0, 255)
        # Calculate cell size
        cell_width = 800 // self.__columns
        cell_height = 600 // self.__lines

        draw_path = False
        path_index = 0
        elapsed_time = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == KEYDOWN and event.key == K_x:
                    pygame.quit()
                    return

            screen.fill(BLACK)  # Clear the screen

            # Draw the maze
            # Draw the maze
            for i in range(self.__lines):
                for j in range(self.__columns):
                    rect = pygame.Rect(j * cell_width, i * cell_height, cell_width, cell_height)
                    if self.__matrix[i][j] == self.__minorPath:
                        pygame.draw.rect(screen, PATH, rect)
                    elif self.__matrix[i][j] == self.__block:
                        pygame.draw.rect(screen, WALL, rect)
                    elif (i, j) == startNode:  # Highlight start node
                        pygame.draw.rect(screen, GREEN, rect)
                    elif (i, j) == endNode:  # Highlight end node
                        pygame.draw.rect(screen, MAGENTA, rect)
                    else:
                        pygame.draw.rect(screen, BACKGROUND, rect)   

            # Draw the path
            if self.__dist[vEnd] != self.INFINITY and path_index < len(shortestPath):
                node = shortestPath[path_index]
                rect = pygame.Rect(node[1] * cell_width, node[0] * cell_height, cell_width, cell_height)
                pygame.draw.rect(screen, BLUE, rect)
                path_index += 1

            pygame.display.flip()
            clock.tick(30)
            elapsed_time += clock.get_time() / 1000
    
    def GetNeighbours(self, line, column, excludeBlock=True):
        neighbours = []
        delta = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for (x, y) in delta:
            if (line+x <= 0 or line+x >= len(self.__matrix) - 1 or column+y <= 0 or column+y >= len(self.__matrix[0]) - 1
                    or (self.__matrix[line+x][column+y] == self.__block and excludeBlock)):
                continue
            else:
                neighbours.append((line+x, column+y, 1))
        return neighbours
    
    def CreateMaze(self, vStart):  # Using Kruskal
        maze = set()
        nodeStack = set()
        notValidNodes = set()
        currentNode = vStart
        nodeStack.add(currentNode)

        while (nodeStack):
            maze.add(currentNode)
            self.__matrix[currentNode[0]][currentNode[1]] = self.__freePath
            neighbours = self.GetNeighbours(
                currentNode[0], currentNode[1], False)
            neighbours = [(element[0], element[1]) for element in neighbours]
            neighbours = list(set(neighbours) - notValidNodes)
            while (True):
                if (not neighbours):
                    break
                found = True
                nextNode = random.choice(neighbours)
                nextNeighbours = self.GetNeighbours(
                    nextNode[0], nextNode[1], False)
                for element in nextNeighbours:
                    if ((element[0:2] in maze) and not (element[0:2] == currentNode)):
                        found = False
                if (found):
                    break
                else:
                    neighbours.remove(nextNode)

            if (found):
                nodeStack.add(currentNode)
                currentNode = nextNode[0:2]
            else:
                notValidNodes.add(currentNode)
                currentNode = nodeStack.pop()

    def CreateMatrix(self):
        return [['▣'] * self.__columns for i in range(self.__lines)]


# Set the desired size of the maze
lines = 60
columns = 80

# Set the start and end nodes
startNode = (random.randint(1, 29), random.randint(1, 40))
endNode = (random.randint(30, 60), random.randint(41, 80))

# Create and solve the maze using Maze
graph = Maze(lines, columns)
graph.DjikstraShotestPath(startNode, endNode)
