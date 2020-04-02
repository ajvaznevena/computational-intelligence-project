from pygame import key
from pygame.locals import *

MOVE = 20


def checkInput(player):
    if player.gameStatus == 0:
        if key.get_pressed()[K_LEFT]:
            player.angle = 180
            player.movex = -MOVE

        if key.get_pressed()[K_RIGHT]:
            player.angle = 0
            player.movex = MOVE

        if key.get_pressed()[K_UP]:
            player.angle = 90
            player.movey = -MOVE

        if key.get_pressed()[K_DOWN]:
            player.angle = 270
            player.movey = MOVE

    elif player.gameStatus == 1 or player.gameStatus == 2:
        if key.get_pressed()[K_SPACE]:
            return 1

    else:
        print("This shouldn't happen :(")
