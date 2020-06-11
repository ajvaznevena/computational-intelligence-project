from algorithms.rl.grid_config import *
from maps import checkMovePoint


class Player:

    def __init__(self):
        self.x, self.y = (30, 470)
        self.movex, self.movey = (0, 0)
        self.angle = 0
        self.score = 0
        self.chasing = False
        self.chasingLast = 0

    def getScore(self):
        return self.score

    def getChasing(self):
        return self.chasing

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
        checkMovePoint(self)
        self.x += self.movex
        self.y += self.movey
        self.movex = 0
        self.movey = 0
        self.angle = 0

        self.chasingLast += 1 if self.chasing else 0

        if self.chasingLast == FIVE_SECS:
            self.chasingLast = 0
            self.chasing = False

    def caught(self, ghost):
        return int(self.y // CELL_SIZE) == int(ghost.y // CELL_SIZE) \
               and int(self.x // CELL_SIZE) == int(ghost.x // CELL_SIZE)

    def eatPill(self, dots):
        for dot in dots:
            if int(self.y // CELL_SIZE) == dot.i and int(self.x // CELL_SIZE) == dot.j and not dot.eaten:
                if dot.dotType == 1:
                    self.score += REGULAR_PILL_CODE
                    dot.eaten = True

                elif dot.dotType == 2:
                    self.score += BIG_PILL_CODE
                    self.chasing = True
                    dot.eaten = True
