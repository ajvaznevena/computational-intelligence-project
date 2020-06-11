from algorithms.ghost_interface import AlgorithmInterface, graph


class AStar(AlgorithmInterface):

    def __init__(self, ghost, player):
        super().__init__()
        self.ghost = ghost
        self.player = player

    def run(self):
        start = self.pixelToGrid((self.ghost.x, self.ghost.y))
        startNameKey = self.getNodeName(start)

        goal = self.get_goal(self.ghost.index)
        goalNameKey = self.getNodeName(goal)

        openset = set()
        openset.add(startNameKey)
        closedset = set()

        distances = {startNameKey: 0}
        parents = {startNameKey: startNameKey}

        while len(openset) > 0:
            n = None

            for v in openset:
                if n is None or distances[v] + AStar.manhattan(v, goalNameKey) < \
                                distances[n] + AStar.manhattan(n, goalNameKey):
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
                    distances[m] = distances[n] + weight
                else:
                    if distances[m] > distances[n] + weight:
                        distances[m] = distances[n] + weight
                        parents[m] = n

                        if m in closedset:
                            closedset.remove(m)
                            openset.add(m)

            openset.remove(n)
            closedset.add(n)

        print("Path doesn't exist")
        return None

    @staticmethod
    def manhattan(v_coords, goal):
        vX, vY = AlgorithmInterface.getCoordsFromName(v_coords)
        finishX, finishY = AlgorithmInterface.getCoordsFromName(goal)

        return abs(vX - finishX) + abs(vY - finishY)