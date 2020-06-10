from pygame import image, Color
from key_input import *

moveImage = image.load('images/move_map.png')
dotImage = image.load('images/dot_map.png')


# check if player can move by desired (movex, movey)
def checkMovePoint(player):
    global moveImage

    if player.x + player.movex < 0:
        player.x = 590

    if player.x + player.movex >= 600:
        player.x = 10

    if moveImage.get_at((int(player.x + player.movex), int(player.y + player.movey))) != Color('black'):
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


# get directions where ghost can move
def getDirections(ghost):
    global moveImage
    directions = 4*[False]  # up, down, right, left

    if ghost.x - 16 < 0:
        ghost.x = 600
    if ghost.x + 16 >= 600:
        ghost.x = 0

    # check if ghost can move up
    if moveImage.get_at((int(ghost.x), int(ghost.y - MOVE))) == Color("black"):
        directions[0] = True

    # check if ghost can move down
    if moveImage.get_at((int(ghost.x), int(ghost.y + MOVE))) == Color("black"):
        directions[1] = True

    # check if ghost can move right
    if moveImage.get_at((int(ghost.x + MOVE), int(ghost.y))) == Color("black"):
        directions[2] = True

    # check if ghost can move left
    if moveImage.get_at((int(ghost.x - MOVE), int(ghost.y))) == Color("black"):
        directions[3] = True

    return directions
