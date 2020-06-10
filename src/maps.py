from pygame import image, Color
from key_input import *
from grid.get_grid import get_grid

dotImage = image.load('images/dot_map.png')


# check if player can move by desired (movex, movey)
def checkMovePoint(player):
    if player.x + player.movex < 0:
        player.x = 590

    if player.x + player.movex >= 600:
        player.x = 10

    grid = get_grid()
    grid_x = int((player.x + player.movex) // 20)
    grid_y = int((player.y + player.movey) // 20)

    if grid[grid_y][grid_x] != 1.0:
        player.movex = player.movey = 0


# get which dot to draw
def checkDotPoint(pos):

    # small dot
    if dotImage.get_at((int(pos[0]), int(pos[1]))) == Color('black'):
        return 1

    # power dot
    elif dotImage.get_at((int(pos[0]), int(pos[1]))) == Color('red'):
        return 2

    else:
        return 0
