import random
<<<<<<< HEAD
from src.algorithms.ghost_interface import AlgorithmInterface
from src.algorithms.a_star import AStar
from src.grid.get_grid import get_grid

from src.algorithms.ghost_interface import graph
=======
from algorithms.algorithm_interface import AlgorithmInterface, graph
from algorithms.help_functions import *
from grid.get_grid import get_grid
>>>>>>> 65aade3603af24c81afdb1289d291bf0769c3632


class GeneticAlgorithm(AlgorithmInterface):

    def __init__(self, ghost, player):
        super().__init__()
        self.ghost = ghost
        self.player = player
        self.max_iter = 300
        self.populationSize = 50
        self.eliteSize = 16    # ~33% of population size

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

                # self.crossover(population[k1], population[k2], newPopulation[i], newPopulation[i + 1])

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
        child1.code = (parent1.code[0], parent2.code[1])
        child2.code = (parent2.code[0], parent1.code[1])
        child1.correctNonFeasible()
        child2.correctNonFeasible()

    def mutation(self, individual):
        nodeName = getNodeName(individual.code)
        if random.random() <= 0.05:
            neighbors = graph.get_neighbors(nodeName)
            neighborNameKey = random.choice(neighbors)[0]
            individual.code = getCoordsFromName(neighborNameKey)

    def getNextStep(self):
        bestIndividual = self.run()
        return getNodeName(bestIndividual.code)


class Individual(AlgorithmInterface):

    def __init__(self, ghost, player):
        super().__init__()
        self.ghost = ghost
        self.player = player
        self.code = self.getCode()        # hromozom je trenutna pozicija
        self.correctNonFeasible()
        self.fitness = 600         # TODO odrediti najveci broj

    def __lt__(self, other):
        return self.fitness < other.fitness

    def correctNonFeasible(self):
        grid = get_grid()
        if grid[self.code[0]][self.code[1]] == 0:
            self.code = (random.randrange(1, 30), random.randrange(0,29))       # ako sam opet ubola lose pozicije, pozovi opet
            self.correctNonFeasible()

<<<<<<< HEAD
=======
    def getNextStep(self):
        pass

>>>>>>> 65aade3603af24c81afdb1289d291bf0769c3632
    def fitnessFunction(self):
        # sto je manje rastojanje do pakmana, to je fitnes bolji
        startNodeNameKey = getNodeName(self.code)
        goal = self.getGoal(self.ghost.index)
<<<<<<< HEAD
        goalNameKey = AlgorithmInterface.getNodeName(goal)
        return AStar.manhattan(startNodeNameKey, goalNameKey)

    def getCode(self):
        return AlgorithmInterface.pixelToGrid((self.ghost.x, self.ghost.y))

    def getNextStep(self):
        return
=======
        goalNameKey = getNodeName(goal)
        return manhattanDistance(startNodeNameKey, goalNameKey)

    def getCode(self):
        return pixelToGrid((self.ghost.x, self.ghost.y))
>>>>>>> 65aade3603af24c81afdb1289d291bf0769c3632
