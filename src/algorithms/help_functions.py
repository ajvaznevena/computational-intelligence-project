from graph import create_graph


def pixelToGrid(node):
    # this is safe because player and ghosts only move on value 1 in grid
    return int(node[1] // 20), int(node[0] // 20)


def getNodeName(node):
    return "n" + str(node[0]) + "_" + str(node[1])


def getCoordsFromName(name):
    index = name.find('_')
    coordX = int(name[1:index])
    coordY = int(name[index + 1:])

    return coordX, coordY


def findShortestPath(startNameKey, goalNameKey):
    """ Based on A* """
    graph = create_graph()

    openset = set()
    openset.add(startNameKey)
    closedset = set()

    distances = {startNameKey: 0}
    parents = {startNameKey: startNameKey}

    while len(openset) > 0:
        n = None

        for v in openset:
            if n is None or distances[v] + manhattanDistance(v, goalNameKey) < \
                    distances[n] + manhattanDistance(n, goalNameKey):
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


def manhattanDistance(pos, goal):
    posX, posY = getCoordsFromName(pos)
    goalX, goalY = getCoordsFromName(goal)

    return abs(posX - goalX) + abs(posY - goalY)