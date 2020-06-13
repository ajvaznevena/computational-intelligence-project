from algorithms.rl.grid_config import *
from maps import checkMovePoint


class Player:

    def __init__(self):
        self.x, self.y = (WIDTH / 2 - CELL_SIZE / 2, 490)
        self.movex, self.movey = (0, 0)
        self.angle = 0
        self.score = 0
        self.notValid = False

    def getScore(self):
        return self.score

    def moveLeft(self):
        self.angle = 180
        self.movex = -CELL_SIZE
        self.move()

    def moveRight(self):
        self.angle = 0
        self.movex = CELL_SIZE
        self.move()

    def moveUp(self):
        self.angle = 90
        self.movey = -CELL_SIZE
        self.move()

    def moveDown(self):
        self.angle = 270
        self.movey = CELL_SIZE
        self.move()

    def move(self):
        self.notValid = True if not checkMovePoint(self) else False

        self.x += self.movex
        self.y += self.movey
        self.movex = 0
        self.movey = 0
        self.angle = 0

    def caught(self, ghost):
        return int(self.y // CELL_SIZE) == int(ghost.y // CELL_SIZE) \
               and int(self.x // CELL_SIZE) == int(ghost.x // CELL_SIZE)

    def eatPill(self, dots):
        for dot in dots:
            if int(self.y // CELL_SIZE) == dot.i and int(self.x // CELL_SIZE) == dot.j:
                if dot.dotType == 1:
                    self.score += 10
                    dots.remove(dot)
                    # return False
                    return REGULAR_PILL_REWARD

                elif dot.dotType == 2:
                    self.score += 50
                    dot.eaten = True
                    # return True
                    return BIG_PILL_REWARD

        return -1
        # return False

    def eatGhost(self, ghosts, chasing):
        if not chasing:
            return 0

        for ghost in ghosts:
            if int(self.y // CELL_SIZE) == int(ghost.y // CELL_SIZE) and int(self.x // CELL_SIZE) == int(ghost.x // CELL_SIZE):
                self.score += 200
                ghost.restart()
                return GHOST_EAT_REWARD

        return 0