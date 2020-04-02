import random
from algorithms.ghost_interface import AlgorithmInterface


class GeneticAlgorithm(AlgorithmInterface):

    def __init__(self, ghost):
        super().__init__()
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