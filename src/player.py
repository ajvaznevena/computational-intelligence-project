from pgzero.builtins import Actor
from pgzero.animation import animate
import key_input
from maps import checkMovePoint

import sys


class Player(Actor):

    def __init__(self, img):
        super().__init__(img)

        self.pos = 290, 490
        self.lives = 3
        self.score = 0
        self.gameStatus = 0
        self.angle = 0
        self.movex = 0
        self.movey = 0
        self.inputEnabled = True
        self.eatAnimation = 0
        self.died = False

    def inputEnable(self):
        self.movex = self.movey = 0
        self.inputEnabled = True

    def getImageAndDraw(self):
        angle = self.angle

        self.eatAnimation = (self.eatAnimation + 1) % 10

        # if player died stop animation
        if self.died:
            self.draw()
            return

        if self.eatAnimation < 6 and (self.movex != 0 or self.movey != 0):
            if angle != 180:
                self.image = "pacman"
            else:
                self.image = "pacman_r"
        else:
            if angle != 180:
                self.image = "pacman_eat"
            else:
                self.image = "pacman_eat_r"     # only going left is not possible using first image, due to rotation

        self.angle = angle  # rotate image
        self.draw()

    def caught(self, ghost, chasing):
        if self.colliderect(ghost) and not chasing:
            self.died = True

        return self.colliderect(ghost)

    def restart(self):
        self.gameStatus = 0
        self.x = 290
        self.y = 490
        self.angle = 0
        self.died = False

    def update(self):
        if self.gameStatus == 0:  # player is moving
            if self.inputEnabled:
                key_input.checkInput(self)
                checkMovePoint(self)

                if self.movex or self.movey:
                    self.inputEnabled = False
                    animate(self, pos=(self.x + self.movex, self.y + self.movey),
                            duration=1 / 3, tween='linear', on_finished=self.inputEnable)

        elif self.gameStatus == 1:  # player caught
            i = key_input.checkInput(self)
            if i == 1:
                self.restart()

            return

        elif self.gameStatus == 2:
            i = key_input.checkInput(self)
            if i == 1:
                print("GAME OVER")
                sys.exit(0)

        else:
            i = key_input.checkInput(self)
            if i == 1:
                sys.exit(0)