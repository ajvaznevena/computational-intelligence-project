from datetime import datetime

import pgzrun
import sys
from pgzero.animation import animate

import key_input
import maps
import ghost_interface
from game_config import *


def draw():
    screen.clear()
    screen.blit('colour_map', (0, 0))

    # draw player
    getPlayerImage()
    player.draw()

    # drawing dots
    for d in dots:
        if d.collidepoint((player.x, player.y)):
            sounds.pacman_eat.play()
            player.score += 10
            dots.remove(d)
            break

    for d in dots:
        d.draw()

    if len(dots) == 0:
        player.gameStatus = 2

    # drawing ghosts
    for g in ghosts:
        g.draw()
        if player.gameStatus == 0:
            if caught(g):
                player.gameStatus = 1

    if player.lives == 0:
        player.gameStatus = 3

    if player.gameStatus == 3:
        drawCentreText("GAME OVER")
    if player.gameStatus == 2:
        drawCentreText("LEVEL CLEARED!\nPress Space\nto Continue")
    if player.gameStatus == 1:
        drawCentreText("CAUGHT!\nPress Space\nto Continue")
        sounds.pacman_death.play()

    # moveGhosts()  # TODO


def drawCentreText(msg):
    screen.draw.text(msg, center=(300, 300), owidth=0.5, ocolor=(255, 255, 255), color=(255, 64, 0), fontsize=60)


def drawGraph(i, j):
    screen.draw.text("X", center=(i*CELLS_PER_INT, j*CELLS_PER_INT), color="red")


def update():
    if player.gameStatus == 0:
        if player.inputEnabled:
            key_input.checkInput(player)
            maps.checkMovePoint(player)

            if player.movex or player.movey:
                player.inputEnabled = False
                animate(player, pos=(player.x + player.movex, player.y + player.movey),
                        duration=1/SPEED, tween='linear', on_finished=inputEnable)

    elif player.gameStatus == 1:
        i = key_input.checkInput(player)

        if i == 1:
            player.gameStatus = 0
            player.x = 290
            player.y = 490
            player.angle = 0

    elif player.gameStatus == 2:
        i = key_input.checkInput(player)

        if i == 1:
            init()


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
        player.lives -= 1
        return True
    else:
        return False


def init():
    music.play('background_music')
    music.set_volume(0.3)

    initPlayer()
    initDots()
    initGhosts()


def initPlayer():
    inputEnable()

    player.pos = 290, 490
    player.lives = 3
    player.score = 0
    player.gameStatus = 0
    player.angle = 0


def inputEnable():
    player.movex = player.movey = 0
    player.inputEnabled = True


def initDots():
    for i in range(30):
        for j in range(29):
            color = maps.checkDotPoint(10 + i*20, 10 + j*20)

            if color == 1:
                dot = Actor("dot", (10 + i*20, 10 + j*20))
                dot.type = 1
                dots.append(dot)

            elif color == 2:
                dot = Actor("power", (10 + i*20, 10 + j*20))
                dot.type = 2
                dots.append(dot)


def initGhosts():
    for i in range(4):
        ghost = Actor("ghost" + str(i+1), (270 + i*20, 290))
        ghosts.append(ghost)

        # depending on which algorithm user selected ghosts algorithm is being initialised
        if algorithm == 'A*':
            ghost.algorithm = ghost_interface.AStar(ghost, player, grid)    # TODO
        else:
            print("Bad algorithm chosen, try again :(")
            sys.exit(1)


def moveGhosts():
    for g in ghosts:
        # because all algorithms implement the same interface we can call getNextStep
        xn, yn = g.algorithm.getNextStep(g, player, grid)   # TODO
        g.x = xn
        g.y = yn
        g.draw()


# TODO da ne smara svaki put, za sad imamo samo A* pa ne mora da se unosi :D
algorithm = 'A*'
# algorithm = input("Enter which algorithm to use for ghosts: ")
init()
pgzrun.go()
