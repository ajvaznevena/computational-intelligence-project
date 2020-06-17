from algorithms.algorithm_interface import AlgorithmInterface, graph
from algorithms.help_functions import *


class Dfs(AlgorithmInterface):

    def __init__(self, ghost, player):
        super().__init__()
        self.ghost = ghost
        self.player = player

    def run(self):
        start = pixelToGrid((self.ghost.x, self.ghost.y))
        startNameKey = getNodeName(start)

        goal = pixelToGrid((self.player.x, self.player.y))
        goalNameKey = getNodeName(goal)

        visited = set()
        stack = [(startNameKey, [startNameKey])]
        while stack:
            v,path = stack.pop()
            if v not in visited:
                if v == goalNameKey:
                    return path
                visited.add(v)
                for n,w in graph.get_neighbors(v):
                    stack.append((n, path+[n]))


    def getNextStep(self):
        goal = self.getGoal(self.ghost.index)
        self.goalNameKey = getNodeName(goal)

        if self.ghost.path == [] or self.ghost.path[-1] != self.goalNameKey:
            path = self.run()

            if path is None:
                print("Error :(")
                sys.exit(1)

            self.ghost.path = path
            self.goalNameKey = self.ghost.path[-1] if self.ghost.path != [] else ''
        else:
            # if goal did not change, we dont'h have to recalculate path again
            self.ghost.path.pop(0)

        if len(self.ghost.path) == 0:
            return None
        else:
            return self.ghost.path[0]
