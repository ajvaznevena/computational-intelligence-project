from algorithms.a_star import AStar

import time


class Ghost:

    def __init__(self, x, y, i, seconds, player):
        self.x = x
        self.y = y
        self.index = i
        self.path = []
        self.algorithm = AStar(self, player)
        self.time = time.time()
        self.seconds = seconds


def initGhosts():
    ghosts = []

    for i in range(1, 5, 1):
        ghost = Ghost(270 + (i-1) * 20, 290, i, (i-1) * 3)

        if i == 3:
            ghost.path.append("n1_1")
        ghosts.append(ghost)

    return ghosts


def moveGhosts(ghosts):
    for ghost in ghosts:
        if time.time() - ghost.time >= ghost.seconds:
            node = ghost.algorithm.getNextStep()
            if node is None:
                return

            index = node.find('_')
            ghost.x = int(node[index + 1:]) * 20 + 10
            ghost.y = int(node[1:index]) * 20 + 10
