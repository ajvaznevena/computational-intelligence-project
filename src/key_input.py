from pygame import key
from pygame.locals import *

MOVE = 20


def checkInput(player):
    if key.get_pressed()[K_LEFT]:
        player.angle = 180
        player.movex = -MOVE

    elif key.get_pressed()[K_RIGHT]:
        player.angle = 0
        player.movex = MOVE

    elif key.get_pressed()[K_UP]:
        player.angle = 90
        player.movey = -MOVE

    elif key.get_pressed()[K_DOWN]:
        player.angle = 270
        player.movey = MOVE

    elif key.get_pressed()[K_SPACE]:
        return 1

    return 0
