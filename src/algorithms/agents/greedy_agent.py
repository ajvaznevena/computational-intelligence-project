from algorithms.help_functions import *


class GreedyAgent:

    def __init__(self):
        self.path = []

    def actBestAction(self, player, dots):

        if not self.path:
            dot = GreedyAgent.closestPill(player, dots)
            playerName = getNodeName(pixelToGrid((player.x, player.y)))
            dotName = getNodeName(pixelToGrid((dot.x, dot.y)))
            self.path = findShortestPath(playerName, dotName)

        nextNode = self.path[0]
        self.path.pop(0)

        currentI, currentJ = pixelToGrid((player.x, player.y))
        nextI, nextJ = getCoordsFromName(nextNode)

        if currentI - nextI < 0:
            return 1    # down
        elif currentI - nextI > 0:
            return 0    # up

        if currentJ - nextJ < 0:
            return 3    # right
        elif currentJ - nextJ > 0:
            return 2    # left

    @staticmethod
    def closestPill(player, dots):
        minDist = float('Inf')
        closest = None

        for dot in dots:
            if abs(player.x - dot.x) + abs(player.y - dot.y) < minDist:
                closest = dot
                minDist = abs(player.x - dot.x) + abs(player.y - dot.y)

        return closest