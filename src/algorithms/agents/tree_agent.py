from abc import ABC, abstractmethod

from algorithms.agents.ghost import Ghost
from algorithms.agents.player import Player
from algorithms.help_functions import *
from algorithms.agents.grid_config import WIDTH, HEIGHT
from algorithms.agents.ghost import moveGhosts
from graph import create_graph

MIN_DIST = 5
NUM_OF_STEPS = 4


class Node(ABC):

    @abstractmethod
    def run(self, player, ghosts, dots, chasing):
        pass


class If(Node):

    def __init__(self):
        self.sequence = None
        self.elseNode = None

    def addSequence(self, seq):
        self.sequence = seq

    def addElseNode(self, node):
        self.elseNode = node

    def run(self, player, ghosts, dots, chasing):
        action = self.sequence.run(player, ghosts, dots, chasing)
        if action is None:
            return self.elseNode.run(player, ghosts, dots, chasing)

        return action


class Sequence(Node):

    def __init__(self):
        self.boolExpression = None
        self.doNodes = []

    def addBoolExpression(self, be):
        self.boolExpression = be

    def addDoNode(self, node):
        self.doNodes.append(node)

    def run(self, player, ghosts, dots, chasing):
        if self.boolExpression.checkValue(player, ghosts, dots, chasing):
            for doNode in self.doNodes:
                return doNode.run(player, ghosts, dots, chasing)
        else:
            return None


class BoolExpression(ABC):

    @abstractmethod
    def checkValue(self, player, ghosts, dots, chasing):
        pass


class GhostClose(BoolExpression):

    def checkValue(self, player, ghosts, dots, chasing):
        """ Checks if ghost is MIN_DIST fields from player (manhattan distance) """

        minDist = float('Inf')

        (playerI, playerJ) = pixelToGrid((player.x, player.y))
        for ghost in ghosts:
            (ghostI, ghostJ) = pixelToGrid((ghost.x, ghost.y))

            distFromPlayer = abs(playerI - ghostI) + abs(playerJ - ghostJ)
            if distFromPlayer < minDist:
                minDist = distFromPlayer

        if minDist < MIN_DIST:
            return True
        else:
            return False


class GhostScared(BoolExpression):

    def checkValue(self, player, ghosts, dots, chasing):
        return chasing


class ChaseGhost(Node):

    def __init__(self):
        self.path = []

    def run(self, player, ghosts, dots, chasing):
        """ Chase closest ghost """

        print('CHASE GHOST!')
        minDist = float('Inf')
        closestGhost = None

        for ghost in ghosts:
            if abs(player.x - ghost.x) + abs(player.y - ghost.y) < minDist:
                closestGhost = ghost
                minDist = abs(player.x - ghost.x) + abs(player.y - ghost.y)

        goalName = getNodeName(pixelToGrid((closestGhost.x, closestGhost.y)))

        if self.path == [] or self.path[-1] != goalName:
            playerName = getNodeName(pixelToGrid((player.x, player.y)))
            ghostName = getNodeName(pixelToGrid((closestGhost.x, closestGhost.y)))
            self.path = findShortestPath(playerName, ghostName)

        nextNode = self.path[0]
        self.path.pop(0)

        return nextNode


class AvoidGhost(Node):

    def run(self, player, ghosts, dots, chasing):
        print('RUN')

        # using quadrants tactics
        # minDist = float('Inf')
        # closestGhost = None
        #
        # for ghost in ghosts:
        #     if abs(player.x - ghost.x) + abs(player.y - ghost.y) < minDist:
        #         closestGhost = ghost
        #         minDist = abs(player.x - ghost.x) + abs(player.y - ghost.y)
        #
        # goalName = getNodeName(AvoidGhost.getClosestGhostOppositeQuadrant(closestGhost))
        #
        # if self.path == [] or self.path[-1] != goalName:
        #     playerName = getNodeName(pixelToGrid((player.x, player.y)))
        #     self.path = findShortestPath(playerName, goalName)
        #
        # nextNode = self.path[0]
        # self.path.pop(0)
        # return nextNode

        # using branch and bound tactics
        path = self.playInAdvance(player, ghosts)

        if path:
            return path[0]
        else:
            return None

    @staticmethod
    def getClosestGhostOppositeQuadrant(ghost):
        if ghost.x < WIDTH / 2 and ghost.y < HEIGHT / 2:
            return int(HEIGHT // 20) - 2, int(WIDTH // 20) - 2
        elif ghost.x >= WIDTH / 2 and ghost.y < HEIGHT / 2:
            return int(HEIGHT // 20) - 2, 1
        elif ghost.x < WIDTH / 2 and ghost.y >= HEIGHT / 2:
            return 1, int(WIDTH // 20) - 2
        else:
            return 1, 1

    def playInAdvance(self, player, ghosts):
        """ Branch and bound based algorithm """
        graph = create_graph()

        visited = set([])

        startNode = getNodeName(pixelToGrid((player.x, player.y)))
        visited.add(startNode)
        path = [startNode]

        bestValue = -1
        bestPath = []
        while len(path) > 0:

            n = path[-1]

            has_unvisited = False

            neighbours = graph.get_neighbors(n)

            if n == 'n14_0':
                neighbours.append(('n14_29', 1))
            elif n == 'n14_29':
                neighbours.append(('n14_0', 1))

            for (m, weight) in neighbours:
                if m not in visited:
                    path.append(m)
                    visited.add(m)
                    has_unvisited = True
                    break

            if not has_unvisited:
                path.pop()
                continue

            steps = self.getStepsFromPath(path)

            branchValue = AvoidGhost.evaluateStateWithSteps(player, ghosts, steps)
            if branchValue == 0:
                path.pop()
                continue

            if len(path) == NUM_OF_STEPS:
                if branchValue > bestValue:
                    bestValue = branchValue
                    bestPath = [n for n in path]

                path.pop()

        if bestPath:
            bestPath.pop(0)

        return bestPath

    @staticmethod
    def getStepsFromPath(path):
        """ From sequence of nodes returns steps between each two """
        steps = []

        for i in range(len(path)):
            prevNode = None
            if i != 0:
                prevNode = path[i-1]

            nextNode = path[i]

            if prevNode is not None and nextNode is not None:
                prevI, prevJ = getCoordsFromName(prevNode)
                nextI, nextJ = getCoordsFromName(nextNode)

                if prevI - nextI < 0:
                    steps.append(1)  # down
                elif prevI - nextI > 0:
                    steps.append(0)  # up

                if prevJ - nextJ < 0:
                    steps.append(3)  # right
                elif prevJ - nextJ > 0:
                    steps.append(2)  # left

        return steps

    @staticmethod
    def evaluateStateWithSteps(player, ghosts, steps):
        ghostsCopy = [Ghost(g.x, g.y, g.index, (g.index-1) * 6, player, g.time) for g in ghosts]
        playerCopy = Player(player.x, player.y)
        actions = {
            0: playerCopy.moveUp,
            1: playerCopy.moveDown,
            2: playerCopy.moveLeft,
            3: playerCopy.moveRight,
        }

        for step in steps:
            actions.get(step)()

            # moveGhosts(ghostsCopy)

            for ghost in ghostsCopy:
                if int(playerCopy.y // 20) == int(ghost.y // 20) \
                        and int(playerCopy.x // 20) == int(ghost.x // 20):
                    return 0

        dist = 0
        for ghost in ghostsCopy:
            dist += abs(playerCopy.x - ghost.x) + abs(playerCopy.y - ghost.y)

        return dist


class EatPill(Node):

    def __init__(self):
        self.path = []

    def run(self, player, ghosts, dots, chasing):
        print('EAT PILL')

        dot = EatPill.closestPill(player, dots)
        dotName = getNodeName(pixelToGrid((dot.x, dot.y)))

        if self.path == [] or self.path[-1] != dotName:
            playerName = getNodeName(pixelToGrid((player.x, player.y)))
            dotName = getNodeName(pixelToGrid((dot.x, dot.y)))
            self.path = findShortestPath(playerName, dotName)

        nextNode = self.path[0]
        self.path.pop(0)

        return nextNode

    @staticmethod
    def closestPill(player, dots):
        minDist = float('Inf')
        closest = None

        for dot in dots:
            if abs(player.x - dot.x) + abs(player.y - dot.y) <= minDist:
                closest = dot
                minDist = abs(player.x - dot.x) + abs(player.y - dot.y)

        return closest


class Tree:

    def __init__(self):
        self.root = If()

        seq = Sequence()
        seq.addBoolExpression(GhostClose())

        ifNode = If()

        seq2 = Sequence()
        seq2.addBoolExpression(GhostScared())
        seq2.addDoNode(ChaseGhost())

        ifNode.addSequence(seq2)
        ifNode.addElseNode(AvoidGhost())

        seq.addDoNode(ifNode)

        self.root.addSequence(seq)
        self.root.addElseNode(EatPill())

    def search(self, player, ghosts, dots, chasing):
        return self.root.run(player, ghosts, dots, chasing)


class TreeAgent:

    def __init__(self):
        self.tree = Tree()

    def actBestAction(self, player, ghosts, dots, chasing):

        nextNode = self.tree.search(player, ghosts, dots, chasing)

        if nextNode is None:
            print('Wherever I go I will die :(')
            return 0

        currentI, currentJ = pixelToGrid((player.x, player.y))
        nextI, nextJ = getCoordsFromName(nextNode)

        if currentI - nextI < 0:
            return 1  # down
        elif currentI - nextI > 0:
            return 0  # up

        if currentJ - nextJ < 0:
            return 3  # right
        elif currentJ - nextJ > 0:
            return 2  # left

        print('Can not decide, this should not happen :(')
        return 0
