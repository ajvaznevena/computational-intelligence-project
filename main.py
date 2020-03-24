from datetime import datetime
import time
import threading

import pgzrun
import sys
from pgzero.animation import animate

import key_input
import maps
import ghost_interface
from game_config import *


def draw():
    global isChasingMode
    global isInitialized
    screen.clear()
    screen.blit('colour_map', (0, 0))

    # draw player
    getPlayerImage()
    player.draw()

    # drawing dots
    for d in dots:
        if d.collidepoint((player.x, player.y)):
            sounds.pacman_eat.play()
            if d.type == 1:
                player.score += 10
                dots.remove(d)
                break
            else:
                player.score += 20
                dots.remove(d)
                isChasingMode = True
                if not isInitialized:
                    initRunningGhosts()
                isInitialized = True
                measureTime()

    for d in dots:
        d.draw()

    if len(dots) == 0:
        player.gameStatus = 3

    # drawing ghosts
    for g in ghosts:
        g.draw()
        if player.gameStatus == 0:
            if caught(g):
                if not isChasingMode:
                    player.gameStatus = 1

    # drawing running ghosts
    for g in runGhosts:
        if player.collidepoint((g.x, g.y)):
            g.x = 290
            g.y = 290
        g.draw()

    if player.lives == 0:
        player.gameStatus = 2

    if player.gameStatus == 2:
        drawCentreText("GAME OVER")

    if player.gameStatus == 3:
        drawCentreText("YOU WON")

    if player.gameStatus == 1:
        drawCentreText("CAUGHT!\nPress Space\nto Continue")
        sounds.pacman_death.play()

def measureTime():
    thread1 = threading.Thread(target=timer)
    thread1.start()

def timer():
    global isChasingMode
    for i in range(SECONDS):
        time.sleep(1)
    isChasingMode = False

def drawCentreText(msg):
    screen.draw.text(msg, center=(300, 300), owidth=0.5, ocolor=(255, 255, 255), color=(255, 64, 0), fontsize=60)


def update():
    global ghost_move

    if player.gameStatus == 0:  # player is moving
        if player.inputEnabled:
            key_input.checkInput(player)
            maps.checkMovePoint(player)

            if player.movex or player.movey:
                player.inputEnabled = False
                animate(player, pos=(player.x + player.movex, player.y + player.movey),
                        duration=1 / SPEED, tween='linear', on_finished=inputEnable)

    elif player.gameStatus == 1:  # player caught
        i = key_input.checkInput(player)

        if i == 1:
            player.gameStatus = 0
            player.x = 290
            player.y = 490
            player.angle = 0

        return

    elif player.gameStatus == 2:
        i = key_input.checkInput(player)

        if i == 1:
            print("GAME OVER")
            sys.exit(0)

    ghost_move += 1
    if ghost_move == ITER:
        if player.gameStatus != 1 and isChasingMode == False:
            moveGhosts()
        else:
            moveRunningGhosts()
        ghost_move = 0


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
            color = maps.checkDotPoint(10 + i * 20, 10 + j * 20)

            if color == 1:
                dot = Actor("dot", (10 + i * 20, 10 + j * 20))
                dot.type = 1
                dots.append(dot)

            elif color == 2:
                dot = Actor("power", (10 + i * 20, 10 + j * 20))
                dot.type = 2
                dots.append(dot)


def initGhosts():
        for i in range(4):
            ghost = Actor("ghost" + str(i + 1), (270 + i * 20, 290))
            ghost.index = i + 1
            ghost.path = []

            if i == 2:
                ghost.path.append("n1_1")

            ghosts.append(ghost)

            # depending on which algorithm user selected ghosts algorithm is being initialised
            if algorithm == 'A*':
                ghost.algorithm = ghost_interface.AStar(ghost)
            elif algorithm == 'gen':
                ghost.algorithm = ghost_interface.GeneticAlgorithm(ghost)
            else:
                print("Bad algorithm chosen, try again :(")
                sys.exit(1)


def initRunningGhosts():
    for i in range(4):
        ghost = Actor("ghost5", (ghosts[i].x, ghosts[i].y))
        ghost.path = []
        ghost.index = i + 1
        ghost.path.append("n1_1")
        ghost.algorithm = ghost_interface.AStar(ghost)
        runGhosts.append(ghost)


def moveGhosts():
    for g in ghosts:
        # because all algorithms implement the same interface we can call getNextStep
        node = g.algorithm.getNextStep()
        if node is None:
            return

        index = node.find('_')
        g.x = int(node[index + 1:]) * 20 + 10
        g.y = int(node[1:index]) * 20 + 10

        for ghost in runGhosts:
            ghost.x = g.x
            ghost.y = g.y
        g.draw()

        # TODO find out why pink ghost dosn't show over dark blue and fix path

def moveRunningGhosts():
    for g in runGhosts:
        node = g.algorithm.getNextStep()
        if node is None:
            return
        index = node.find('_')
        g.x = int(node[index + 1:]) * 20 + 10
        g.y = int(node[1:index]) * 20 + 10

        for ghost in ghosts:
            ghost.x = g.x
            ghost.y = g.y
        g.draw()



# TODO da ne smara svaki put, za sad imamo samo A* pa ne mora da se unosi :D
algorithm = 'A*'
#algorithm = 'gen'
# algorithm = input("Enter which algorithm to use for ghosts: ")
init()
pgzrun.go()
