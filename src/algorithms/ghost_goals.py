import random
from game_config import *


def lightBlueGoal(self):
    targetX, targetY = 0, 0

    # see where player is moving
    if (player.angle // 90) % 2 == 0:
        targetX = -80 if player.movex < 0 else 80  # 4 * 20
    else:
        targetY = -80 if player.movey < 0 else 80

    gridX, gridY = self.pixelToGrid((player.x + targetX, player.y + targetY))

    if 0 <= gridX < 29 and 0 <= gridY < 30:
        if grid[gridX, gridY]:
            return gridX, gridY

    return self.pixelToGrid((player.x, player.y))


def orangeGoal(self):
    nodesNo = len(graph.adjacency_list)
    r = random.randrange(nodesNo)

    goal = list(graph.adjacency_list.keys())[r]
    return self.getCoordsFromName(goal)


def pinkGoal(self):
    targetX, targetY = 0, 0

    # see where player is moving
    if (player.angle // 90) % 2 == 0:
        targetX = 160 if player.movex < 0 else -160  # 8 * 20
    else:
        targetY = 160 if player.movey < 0 else -160

    tarX, tarY = self.pixelToGrid((player.x + targetX, player.y + targetY))

    if 0 <= tarX < 29 and 0 <= tarY < 30:
        if grid[tarX, tarY]:
            return tarX, tarY

    return self.pixelToGrid((player.x, player.y))