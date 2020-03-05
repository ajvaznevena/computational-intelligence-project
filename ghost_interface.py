from abc import ABC, abstractmethod


class AlgorithmInterface(ABC):

    @abstractmethod
    def getNextStep(self, player, dot, grid):
        pass


class Node:
    def __init__(self, value, point):
        self.value = value
        self.point = point
        self.parent = None
        self.G = 0
        self.H = 0

    def moveCost(self, other):
        return 0 if self.value == '.' else 1


class AStar(AlgorithmInterface):

    def __init__(self, start, goal, grid):
        self.start = start
        self.goal = goal
        self.grid = grid

    def aStar(self, start, goal, grid):
        openset = set()

        closedset = set()
        current = start
        openset.add(current)
        while openset:
            current = min(openset, key = lambda  o: o.G + o.H)
            if current == goal:
                path = []
                while current.parent:
                    path.append(current)
                    current = current.parent
                path.append(current)
                return path[::-1]
            openset.remove(current)
            closedset.add(current)
            for node in self.children(current, grid):
                if node in closedset:
                    continue
                if node in openset:
                    new = current.G + current.moveCost(node)
                    if node.G > new:
                        node.G = new
                        node.parent = current
                else:
                    node.G = current.G + current.moveCost(node)
                    node.H = self.manhattan(node, goal)
                    node.parent = current
                    openset.add(node)

    def manhattan(self, node, goal):
        return abs(node.point[0] - goal.point[0]) + abs(node.point[1]-goal.point[1])

    def children(self, point, grid):
        x, y = point.point
        links = [grid[d[0]][d[1]] for d in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]]
        return [link for link in links if link.value != 'x']

    def getNextStep(self, ghost, player, grid):
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                grid[x][y] = Node(grid[x][y], (x, y))

        path = self.aStar(grid[int(ghost.x)][int(ghost.y)], grid[int(player.x)][int(player.y)], grid)

        for node in path:
            x, y = node.point
            return (x,y)


