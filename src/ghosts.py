from game_config import *
from algorithms.a_star import AStar
from algorithms.genetic_algorithm import GeneticAlgorithm


def initGhosts(algorithm):
    for i in range(4):
        ghost = Actor("ghost" + str(i + 1), (270 + i * 20, 290))
        ghost.index = i + 1
        ghost.path = []

        if i == 2:
            ghost.path.append("n1_1")
        ghosts.append(ghost)

        # depending on which algorithm user selected ghosts algorithm is being initialised
        if algorithm == 'A*':
            ghost.algorithm = AStar(ghost)
        elif algorithm == 'gen':
            ghost.algorithm = GeneticAlgorithm(ghost)
        else:
            print("Bad algorithm chosen, try again :(")
            sys.exit(1)


def initRunningGhosts():
    for i in range(4):
        ghost = Actor("ghost5", (ghosts[i].x, ghosts[i].y))
        ghost.index = i + 1
        runGhosts.append(ghost)


def moveGhosts():
    for g in ghosts:
        # because all algorithms implement the same interface we can call getNextStep
        node = g.algorithm.getNextStep()
        if node is None:
            return

        index = node.find('_')
        g.x = int(node[index + 1:]) * 20 + 10
        g.y = int(node[1:index]) * 20 + 10
        g.draw()

def moveRunningGhosts():
    for g in runGhosts:
        for ghost in ghosts:
            if g.index == ghost.index:
                g.x = ghost.x
                g.y = ghost.y

        g.draw()
