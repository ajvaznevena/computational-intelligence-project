from pygame import key
from pygame.locals import *

from game_constants import CELL_SIZE


def checkInput(player):
    if key.get_pressed()[K_LEFT]:
        moveLeft(player)

    elif key.get_pressed()[K_RIGHT]:
        moveRight(player)

    elif key.get_pressed()[K_UP]:
        moveUp(player)

    elif key.get_pressed()[K_DOWN]:
        moveDown(player)

    elif key.get_pressed()[K_SPACE]:
        return 1

    return 0


def playerMove(player, action):

    if action == 0:
        moveUp(player)

    elif action == 1:
        moveDown(player)

    elif action == 2:
        moveLeft(player)

    elif action == 3:
        moveRight(player)


def moveLeft(player):
    player.angle = 180
    player.movex = -CELL_SIZE


def moveRight(player):
    player.angle = 0
    player.movex = CELL_SIZE


def moveUp(player):
    player.angle = 90
    player.movey = -CELL_SIZE


def moveDown(player):
    player.angle = 270
    player.movey = CELL_SIZE
