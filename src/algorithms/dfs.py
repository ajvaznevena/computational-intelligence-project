from algorithms.algorithm_interface import AlgorithmInterface, graph
from algorithms.help_functions import *


class Dfs(AlgorithmInterface):

    def __init__(self, ghost, player):
        super().__init__()
        self.ghost = ghost
        self.player = player
        self.init = True
        self.path = []

    def run(self):
        start = pixelToGrid((self.ghost.x, self.ghost.y))
        startNameKey = getNodeName(start)

        visited = [startNameKey]
        stack = [startNameKey]
        while stack:
            v = stack[-1]
            if v not in visited:
                visited.append(v)
            removeFromStack = True
            for n,w in graph.get_neighbors(v):
                if n not in visited:
                    stack.append(n)
                    removeFromStack = False
                    break
            if removeFromStack:
                stack.pop()

        return visited


    def getNextStep(self):
        if self.init:
            self.path = self.run()
            self.init = False

        return self.path.pop(0)
