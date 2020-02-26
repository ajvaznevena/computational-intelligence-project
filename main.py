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


def draw():
    screen.clear()
    screen.blit('colour_map', (0,0))
    player.draw()
    getPlayerImage()


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


def init():
    initPlayer()
    music.play('background_music')
    music.set_volume(0.3)


init()
pgzrun.go()
