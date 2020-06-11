from maps import checkMovePoint


class Player:

    def __init__(self):
        self.x = 290
        self.y = 490
        self.movex = 0
        self.movey = 0
        self.angle = 0
        self.lives = 3
        self.score = 0
        self.gameStatus = 0

    def moveLeft(self):
        self.angle = 180
        self.movex = -20

    def moveRight(self):
        self.angle = 0
        self.movex = 20

    def moveUp(self):
        self.angle = 90
        self.movey = -20

    def moveDown(self):
        self.angle = 270
        self.movey = 20

    def caught(self, ghost):
        return int(self.x // 20) == int(ghost.x // 20) and int(self.y // 20) == int(ghost.y // 20)

    def restart(self):
        self.x = 290
        self.y = 490
        self.movex = 0
        self.movey = 0
        self.angle = 0
        self.gameStatus = 0

    def onGameRestart(self):
        self.restart()
        self.lives = 3
        self.score = 0

    def update(self):
        # PAZI: ocekuje da je pomereno
        if self.gameStatus == 0:  # player is moving
            checkMovePoint(self)

        elif self.gameStatus == 1:  # player caught
            self.restart()
