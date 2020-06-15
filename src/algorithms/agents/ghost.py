from algorithms.agents.grid_config import *
from algorithms.a_star import AStar


class Ghost:

    def __init__(self, x, y, i, frames, player):
        self.x = x
        self.y = y
        self.index = i
        self.path = []
        self.algorithm = AStar(self, player)
        self.time = 0
        self.frames = frames

    def restart(self):
        self.x = 290
        self.y = 290
        self.path = []


def initGhosts(player):
    ghosts = []

    for i in range(1, 5, 1):
        ghost = Ghost(270 + (i-1) * CELL_SIZE, HEIGHT / 2, i, (i-1) * THREE_SECS, player)
        if i == 3:
            ghost.path.append("n1_1")
        ghosts.append(ghost)

    return ghosts


def moveGhosts(ghosts):
    for ghost in ghosts:
        if ghost.time >= ghost.frames:
            print("OK")
            node = ghost.algorithm.getNextStep()
            print("OK2")
            if node is None:
                return

            index = node.find('_')
            ghost.x = int(node[index + 1:]) * CELL_SIZE + CELL_SIZE / 2
            ghost.y = int(node[1:index]) * CELL_SIZE + CELL_SIZE / 2

        else:
            ghost.time += 1
