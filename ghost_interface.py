from abc import ABC, abstractmethod

import game_config
import numpy as np

from grid.get_grid import get_grid


class AlgorithmInterface(ABC):

    @abstractmethod
    def getNextStep(self):
        pass

#
# class Node:
#     def __init__(self, value, point):
#         self.value = value
#         self.point = point
#         self.parent = None
#         self.G = 0
#         self.H = 0
#
#     def moveCost(self, other):
#         return 0 if self.value == '.' else 1


class AStar(AlgorithmInterface):

    def __init__(self, ghost, player, graph, index, grid):
        self.ghost = ghost
        self.player = player
        self.graph = graph
        self.index = index
        self.grid = grid

    def aStar(self, start, goal):

        # Blue ghost's goal is player
        # if self.index == 1:
        #     print("Cao!")
        # else:
        #     print("else")

        start = self.pixelToGrid(start)
        startNameKey = "n" + str(start[0]) + "_" + str(start[1])

        goal = self.pixelToGrid(goal)
        goalNameKey = "n" + str(goal[0]) + "_" + str(goal[1])


        openset = set()
        closedset = set()

        current = startNameKey
        openset.add(current)

        # distances
        g = {}
        g[startNameKey] = 0

        parents = {}
        parents[startNameKey] = startNameKey

        while len(openset) > 0:
            n = None
            for v in openset:
                if n == None or g[v] + self.manhattan(v, goalNameKey) < g[n] + self.manhattan(n, goalNameKey):
                    n = v

            if n == None:
                print("Path doesn't exist")
                return None

            if n == goalNameKey:
                path = []
                while parents[n] != n:
                    path.append(n)
                    n = parents[n]
                path.append(startNameKey)
                path.reverse()
                return path

            neighbors = self.graph.get_neighbors(n)


            for (m, weight) in neighbors:
                if m not in openset and m not in closedset:

                    index = m.find('_')
                    mx = int(m[1:index])
                    my = int(m[index + 1:])
                    if self.grid[mx, my]:   # is this necessary????
                        openset.add(m)
                        parents[m] = n
                        g[m] = g[n] + weight
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closedset:
                            closedset.remove(m)
                            openset.add(m)
            openset.remove(n)
            closedset.add(n)

        print("Path doesn't exist")
        return None


    def pixelToGrid(self, node):
        newX = 30*node[0] / game_config.WIDTH
        newY = 29*node[1] / game_config.HEIGHT

        grid = np.array(get_grid())
        rows, columns = grid.shape
        closestNodes = {}

        for i in range(rows):
            for j in range(columns):
                distance = np.sqrt((newX - i)**2 + (newY - j)**2)
                closestNodes[(i,j)] = distance

        sorted(closestNodes.items(), key=lambda x: x[1])

        for k,v in closestNodes.items():
            if grid[k]:
                return k

        return (-1, -1)


    def manhattan(self, v_coords, goal):
        xx = v_coords.find('_')
        v_x = int(v_coords[1:xx])
        v_y = int(v_coords[xx + 1:])

        xx = goal.find('_')
        finish_x = int(goal[1:xx])
        finish_y = int(goal[xx + 1:])

        return abs(v_x - finish_x) + abs(v_y - finish_y)


    def getNextStep(self):
        # Pozivamo astar funkciju i ona treba da nam vrati putanju.
        # Prvi sledeci cvor (path[0]), tj. x i y koordinate treba da se vrate kako bi se duh iscrtao tu

        # aStar prima koordinate pocetka(duha) i koordinate cilja(pakman)
        path = self.aStar((self.ghost.x, self.ghost.y), (self.player.x, self.player.y))
        print(path)
        return path[0]
