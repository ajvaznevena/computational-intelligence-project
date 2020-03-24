from abc import ABC, abstractmethod
import sys
import random

from game_config import *


class AlgorithmInterface(ABC):

    @abstractmethod
    def getNextStep(self):
        pass


class AStar(AlgorithmInterface):

    def __init__(self, ghost):
        self.ghost = ghost

    def run(self):

        start = AStar.pixelToGrid((self.ghost.x, self.ghost.y))
        startNameKey = AStar.getNodeName(start)

        goal = AStar.get_goal(self.ghost.index)
        goalNameKey = AStar.getNodeName(goal)

        openset = set()
        openset.add(startNameKey)
        closedset = set()

        # distances
        g = {startNameKey: 0}
        parents = {startNameKey: startNameKey}

        while len(openset) > 0:
            n = None

            for v in openset:
                if n is None or g[v] + AStar.manhattan(v, goalNameKey) < g[n] + self.manhattan(n, goalNameKey):
                    n = v

            if n is None:
                print("Path doesn't exist")
                return None

            if n == goalNameKey:
                path = []
                while parents[n] != n:
                    path.append(n)
                    n = parents[n]

                path.reverse()
                return path

            for (m, weight) in graph.get_neighbors(n):
                if m not in openset and m not in closedset:
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

    @staticmethod
    def get_goal(index):
        # Red ghost's goal is player (index = 1)
        if index == 1:
            return AStar.pixelToGrid((player.x, player.y))

        # Lightblue ghost's goal is 4 fields ahead player's current postion (index = 2)
        elif index == 2:
            return AStar.lightBlueGoal()

        # Orange ghost's goal is random node (index = 3)
        elif index == 3:
            return AStar.orangeGoal()

        # Pink ghost's goal is 8 fields behind player's current postion (index = 4)
        elif index == 4:
            return AStar.pinkGoal()

    @staticmethod
    def lightBlueGoal():
        targetx, targety = 0, 0

        if (player.angle // 90) % 2 == 0:
            targetx = -80 if player.movex < 0 else 80

        else:
            targety = -80 if player.movey < 0 else 80

        tarx, tary = AStar.pixelToGrid((player.x + targetx, player.y + targety))

        if 0 <= tarx < 29 and 0 <= tary < 30:
            if not grid[tarx, tary]:
                return AStar.pixelToGrid((player.x, player.y))
            else:
                return tarx, tary

        return AStar.pixelToGrid((player.x, player.y))

    @staticmethod
    def orangeGoal():
        nodesNo = len(graph.adjacency_list)
        r = random.randrange(nodesNo)
        goal = list(graph.adjacency_list.keys())[r]
        return AStar.getCoordsFromName(goal)

    @staticmethod
    def pinkGoal():
        targetx, targety = 0, 0

        if (player.angle // 90) % 2 == 0:
            targetx = 160 if player.movex < 0 else -160

        else:
            targety = 160 if player.movey < 0 else -160

        tarx, tary = AStar.pixelToGrid((player.x + targetx, player.y + targety))

        if 0 <= tarx < 29 and 0 <= tary < 30:
            if not grid[tarx, tary]:
                return AStar.pixelToGrid((player.x, player.y))
            else:
                return tarx, tary

        return AStar.pixelToGrid((player.x, player.y))


    @staticmethod
    def pixelToGrid(node):
        # this is safe because player and ghosts only move on value 1 in grid
        return round(node[1] // 20), round(node[0] // 20)

    @staticmethod
    def manhattan(v_coords, goal):
        vX, vY = AStar.getCoordsFromName(v_coords)
        finishX, finishY = AStar.getCoordsFromName(goal)

        return abs(vX - finishX) + abs(vY - finishY)

    @staticmethod
    def getCoordsFromName(str):
        index = str.find('_')
        coordX = int(str[1:index])
        coordY = int(str[index + 1:])

        return coordX, coordY

    @staticmethod
    def getNodeName(node):
        return "n" + str(node[0]) + "_" + str(node[1])

    def getNextStep(self):
        goalNameKey = ""

        if self.ghost.index == 2:
            goal = AStar.lightBlueGoal()
            goalNameKey = AStar.getNodeName(goal)
        elif self.ghost.index == 3:
            if self.ghost.path:
                goal = AStar.getCoordsFromName(self.ghost.path[-1])
                goalNameKey = AStar.getNodeName(goal)
        elif self.ghost.index == 4:
            goal = AStar.pinkGoal()

        else:
            goal = AStar.pixelToGrid((player.x, player.y))
            goalNameKey = AStar.getNodeName(goal)

        # if player did not move we don't need to calculate path again
        # instead, we just give next node in calculated path

        if self.ghost.path == [] or self.ghost.path[-1] != goalNameKey:
            path = self.run()
            # print(path)

            if path is None:
                print("Error :(")
                sys.exit(1)

            self.ghost.path = path
        else:
            self.ghost.path.pop(0)

        if self.ghost.path == []:
            return None
        else:
            return self.ghost.path[0]


class GeneticAlgorithm(AlgorithmInterface):

    def __init__(self, ghost):
        self.ghost = ghost
        self.max_iter = 300

    def run(self):
        population = []
        newPopulation = []
        for i in range(100):
            population.append(Individual(self.ghost))
            newPopulation.append(Individual(self.ghost))

        for iteration in range(self.max_iter):
            population.sort()
            for i in range(30):
                newPopulation[i] = population[i]
            for i in range(30, 100, 2):
                k1 = self.selection(population)
                k2 = self.selection(population)
                self.crossover(population[k1], population[k2], newPopulation[i], newPopulation[i + 1])
                self.mutation(newPopulation[i])
                self.mutation(newPopulation[i + 1])
                newPopulation[i].fitness = newPopulation[i].fitnessFunction()
                newPopulation[i + 1].fitness = newPopulation[i + 1].fitnessFunction()
            population = newPopulation

        return population

    def selection(self, population):
        min = float('inf')
        k = -1
        for i in range(6):
            j = random.randrange(100)
            if population[j].fitness < min:
                min = population[j].fitness
                k = j
        return k

    def crossover(self, parent1, parent2, child1, child2):
        nbResources = len(parent1.code)
        i = random.randrange(nbResources)
        for j in range(i):
            child1.code[j] = parent1.code[j]
            child2.code[j] = parent2.code[j]
        for j in range(i, nbResources):
            child1.code[j] = parent2.code[j]
            child2.code[j] = parent1.code[j]


    def mutation(self, individual):
        nbResources = len(individual.code)
        for i in range(nbResources):
            if random.random() > 0.05:
                continue
            individual.code[i] = not individual.code[i]


    def getNextStep(self):
        pass


class Individual:
    def __init__(self, ghost):
        self.ghost = ghost
        self.fitness = self.fitnessFunction()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def fitnessFunction(self):
        pass


