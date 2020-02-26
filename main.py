import numpy
import pgzrun
import pygame

WIDTH = 600
HEIGHT = 580

player = Actor('pacman_eat')
player.pos = 300, 350


def draw():
    screen.clear()
    screen.blit('colour_map', (0,0))
    player.draw()

def update():
    player.left += 2
    if player.left > WIDTH:
        player.right = 0


def init():
    music.play('background_music')
    music.set_volume(0.3)

init()
pgzrun.go()
