from game_config import *


def initPlayer():
    inputEnable()

    player.pos = 290, 490
    player.lives = 3
    player.score = 0    # TODO: add player score to screen
    player.gameStatus = 0
    player.angle = 0


def inputEnable():
    player.movex = player.movey = 0
    player.inputEnabled = True


def getPlayerImage():
    dt = datetime.now()
    a = player.angle
    tc = dt.microsecond % (500000 / SPEED) / (100000 / SPEED)

    if tc > 2.5 and (player.movex != 0 or player.movey != 0):
        if a != 180:
            player.image = "pacman"
        else:
            player.image = "pacman_r"
    else:
        if a != 180:
            player.image = "pacman_eat"
        else:
            player.image = "pacman_eat_r"
    player.angle = a


def caught(ghost):
    if player.collidepoint((ghost.x, ghost.y)):
        if not isChasingMode:
            player.lives -= 1
        return True
    else:
        return False
