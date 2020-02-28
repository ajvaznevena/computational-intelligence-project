from pygame import key
from pygame.locals import *

MOVEX = 15
MOVEY = 10

def checkInput(player):
    if player.gameStatus == 0:
        if key.get_pressed()[K_LEFT]:
            player.angle = 180
            player.movex = -MOVEX

        if key.get_pressed()[K_RIGHT]:
            player.angle = 0
            player.movex = MOVEX

        if key.get_pressed()[K_UP]:
            player.angle = 90
            player.movey = -MOVEY

        if key.get_pressed()[K_DOWN]:
            player.angle = 270
            player.movey = MOVEY

    elif player.gameStatus == 1:
        if key.get_pressed()[K_SPACE]:
            return 1
    elif player.gameStatus == 2:
        if key.get_pressed()[K_SPACE]:
            return 2
    else:
        print("This shouldn't happen :(")
