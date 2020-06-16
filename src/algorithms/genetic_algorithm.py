import random
import numpy as np

from algorithms.algorithm_interface import AlgorithmInterface, graph
from algorithms.help_functions import *
from grid.get_grid import get_grid
from algorithms.help_functions import pixelToGrid, getNodeName, manhattanDistance


class GeneticAlgorithm(AlgorithmInterface):

    def __init__(self, ghost, player):
        super().__init__()
        self.ghost = ghost
        self.player = player
        self.max_iter = 300
        self.populationSize = 30
        self.eliteSize = 4

    def run(self):
        population = []
        newPopulation = []
        for i in range(self.populationSize):
            population.append(Individual(self.ghost, self.player))
            newPopulation.append(Individual(self.ghost, self.player))

        for iteration in range(self.max_iter):
            population.sort()
            for i in range(self.eliteSize):
                newPopulation[i] = population[i]
            for i in range(self.eliteSize, self.populationSize, 2):
                k1 = self.selection(population)
                k2 = self.selection(population)

                self.crossover(population[k1], population[k2], newPopulation[i], newPopulation[i + 1])

                self.mutation(newPopulation[i])
                self.mutation(newPopulation[i + 1])

                newPopulation[i].fitness = newPopulation[i].fitnessFunction()
                newPopulation[i + 1].fitness = newPopulation[i + 1].fitnessFunction()

            population = newPopulation
        return population[0]

    def selection(self, population):
        min = float('inf')
        k = -1
        for i in range(6):
            j = random.randrange(self.populationSize)
            if population[j].fitness < min:
                min = population[j].fitness
                k = j
        return k

    def crossover(self, parent1, parent2, child1, child2):
        i = random.randrange(0, 3)
        child1.code = parent1.code[0:i] + parent2.code[i:]
        child2.code = parent2.code[0:i] + parent1.code[i:]

    def mutation(self, individual):
        if random.random() <= 0.05:
            place = random.randrange(0, 3)
            individual.code[place] = random.randrange(0, 4)

    def getNextStep(self):
        bestIndividual = self.run()
        return bestIndividual.getNextStep()


class Individual(AlgorithmInterface):

    def __init__(self, ghost, player):
        super().__init__()
        self.ghost = ghost
        self.player = player
        self.code = self.getCode()        # chromosome is 5-step path
        # self.correctNonFeasible()
        self.fitness = float('Inf')

    def __lt__(self, other):
        return self.fitness < other.fitness

    def correctNonFeasible(self):
        grid = get_grid()
        if grid[self.code[0]][self.code[1]] == 0:
            self.code = (random.randrange(1, 28), random.randrange(0,30))
            self.correctNonFeasible()

    def getNextStep(self):
        ghostI, ghostJ = pixelToGrid((self.ghost.x, self.ghost.y))

        if self.code[0] == 0:   # up
            if ghostI != 0:
                ghostI -= 1
        elif self.code[0] == 1:     # down
            if ghostI != 28:
                ghostI += 1
        elif self.code[0] == 2:     # right
            if ghostJ != 0:
                ghostJ -= 1
        elif self.code[0] == 3:     # left
            if ghostJ != 29:
                ghostJ += 1

        return getNodeName((ghostI, ghostJ))

    def fitnessFunction(self):
        # fitness is better when distance is closer
        startNodeNameKey = getNodeName(pixelToGrid((self.ghost.x, self.ghost.y)))
        goal = self.getGoal(self.ghost.index)
        goalNameKey = getNodeName(goal)

        return manhattanDistance(startNodeNameKey, goalNameKey)

    def getCode(self):
        x = []
        for i in range(3):
            x.append(random.randrange(0, 4))
        return x
