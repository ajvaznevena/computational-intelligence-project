from abc import ABC, abstractmethod

from algorithms.help_functions import *
from algorithms.agents.grid_config import WIDTH, HEIGHT, CELL_SIZE


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
        self.doNode = None

    def addBoolExpression(self, be):
        self.boolExpression = be

    def addDoNode(self, node):
        self.doNode = node

    def run(self, player, ghosts, dots, chasing):
        if self.boolExpression.checkValue(player, ghosts, dots, chasing):
            return self.doNode.run(player, ghosts, dots, chasing)
        else:
            return None


class BoolExpression(ABC):

    @abstractmethod
    def checkValue(self, player, ghosts, dots, chasing):
        pass


class GhostClose(BoolExpression):

    def checkValue(self, player, ghosts, dots, chasing):
        minDist = float('Inf')

        for ghost in ghosts:
            if abs(player.x - ghost.x) + abs(player.y - ghost.y) < minDist:
                minDist = abs(player.x - ghost.x) + abs(player.y - ghost.y)

        print(f'MIN DIST: {minDist}')
        if minDist < 200:
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

    def __init__(self):
        self.path = []

    def run(self, player, ghosts, dots, chasing):
        print('RUN')
        minDist = float('Inf')
        closestGhost = None

        for ghost in ghosts:
            if abs(player.x - ghost.x) + abs(player.y - ghost.y) < minDist:
                closestGhost = ghost
                minDist = abs(player.x - ghost.x) + abs(player.y - ghost.y)

        goalName = getNodeName(AvoidGhost.getClosestGhostOppositeQuadrant(closestGhost))

        if self.path == [] or self.path[-1] != goalName:
            playerName = getNodeName(pixelToGrid((player.x, player.y)))
            self.path = findShortestPath(playerName, goalName)

        nextNode = self.path[0]
        self.path.pop(0)

        return nextNode

    @staticmethod
    def getClosestGhostOppositeQuadrant(ghost):
        if ghost.x < WIDTH / 2 and ghost.y < HEIGHT / 2:
            return int(HEIGHT // CELL_SIZE) - 2, int(WIDTH // CELL_SIZE) - 2
        elif ghost.x >= WIDTH / 2 and ghost.y < HEIGHT / 2:
            return int(HEIGHT // CELL_SIZE) - 2, 1
        elif ghost.x < WIDTH / 2 and ghost.y >= HEIGHT / 2:
            return 1, int(WIDTH // CELL_SIZE) - 2
        else:
            return 1, 1


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
            if abs(player.x - dot.x) + abs(player.y - dot.y) < minDist:
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
