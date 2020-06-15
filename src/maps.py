from pygame import image, Color

from key_input import *
from grid.get_grid import get_grid
from game_constants import CELL_SIZE, WIDTH, HEIGHT

dotImage = image.load('images/dot_map.png')


def checkMovePoint(player):
    """ Checks if player can move by selected (movex, movey) """

    if player.x + player.movex < 0:
        player.x = WIDTH - CELL_SIZE / 2

    if player.x + player.movex >= WIDTH:
        player.x = CELL_SIZE / 2

    grid = get_grid()
    grid_x = int((player.x + player.movex) // CELL_SIZE)
    grid_y = int((player.y + player.movey) // CELL_SIZE)

    if grid[grid_y][grid_x] != 1.0:
        player.movex = player.movey = 0
        return False

    return True


def checkDotPoint(pos):
    """ Gets which dot to draw from do map image """

    # small dot
    if dotImage.get_at((int(pos[0]), int(pos[1]))) == Color('black'):
        return 1

    # power dot
    elif dotImage.get_at((int(pos[0]), int(pos[1]))) == Color('red'):
        return 2

    else:
        return 0
