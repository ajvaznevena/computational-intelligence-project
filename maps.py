from pygame import image, Color

moveImage = image.load('images/move_map.png')
dotImage = image.load('images/dot_map.png')


def checkMovePoint(player):
    global moveImage
    if player.x + player.movex < 0:
        player.x = player.x + 600
    if player.x + player.movex >= 600:
        player.x = 0
    if moveImage.get_at((int(player.x + player.movex), int(player.y + player.movey))) != Color('black'):
        player.movex = player.movey = 0

def checkDotPoint(x, y):
    global dotImage
    # small dot
    if dotImage.get_at((int(x), int(y))) == Color('black'):
        return 1

    # power dot
    elif dotImage.get_at((int(x), int(y))) == Color('red'):
        return 2

    else:
        return 0

