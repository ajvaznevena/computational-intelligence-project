import pgzrun
import pygame
from pgzero.animation import animate
from pgzero.builtins import Actor
import maps
import key_input

WIDTH = 600
HEIGHT = 580
SPEED = 3

# Player
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
                animate(player, pos=(player.x + player.movex, player.y + player.movey), duration=1/3, tween='linear', on_finished=inputEnable)

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
    player.inputEnabled = True


def getPlayerImage():
    pass

def init():
    initPlayer()
    music.play('background_music')
    music.set_volume(0.3)


init()
pgzrun.go()
