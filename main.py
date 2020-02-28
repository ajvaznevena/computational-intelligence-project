from datetime import datetime

import pgzrun
from pgzero.animation import animate
from pgzero.builtins import Actor

import key_input
import maps

WIDTH = 600
HEIGHT = 580
SPEED = 3

player = Actor('pacman_eat')
dots = []
ghosts = []

def draw():
    global dots, ghosts

    screen.clear()
    screen.blit('colour_map', (0,0))
    player.draw()
    getPlayerImage()

    # drawing dots
    for d in dots:
        if d.collidepoint((player.x, player.y)):
            sounds.pacman_eat.play()
            player.score += 10
            dots.remove(d)
            break
    for d in dots:
        d.draw()

    # drawing ghosts
    for g in ghosts:
        g.draw()

    # colliding ghost-pacman check
    for g in ghosts:
        # if caught(g):
            # print("OP!")
        print(maps.getDirections(g))


def update():
    global player
    if player.gameStatus == 0:
        if player.inputEnabled:
            key_input.checkInput(player)
            maps.checkMovePoint(player)
            if player.movex or player.movey:
                player.inputEnabled = False
                animate(player, pos=(player.x + player.movex, player.y + player.movey),
                        duration=1/SPEED, tween='linear', on_finished=inputEnable)


def initPlayer():
    inputEnable()
    player.pos = 300, 350
    player.lives = 3
    player.score = 0
    player.gameStatus = 0
    player.movex = player.movey = 0
    player.angle = 0


def inputEnable():
    global player
    player.movex = player.movey = 0
    player.inputEnabled = True


def getPlayerImage():
    global player
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


def initDots():
    global dots

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


def caught(ghost):
    if player.collidepoint((ghost.x, ghost.y)):
        return True
    else:
        return False


def initGhosts():
    global ghosts

    for i in range(4):
        ghost = Actor("ghost"  + str(i+1), (270+i*20 , 290))
        ghosts.append(ghost)

def init():
    initPlayer()
    music.play('background_music')
    music.set_volume(0.3)
    initDots()
    initGhosts()


init()
pgzrun.go()
