from pygame import image, Color

moveImage = image.load('images/move_map.png')
dotImage = image.load('images/dot_map.png')


def checkMovePoint(player):
    global moveImage
    if player.x + player.movex < 0:
        player.x = player.x + 600
    if player.x + player.movex > 600:
        player.x = player.x - 600
    if moveImage.get_at((int(player.x + player.movex), int(player.y + player.movey))) != Color('black'):
        player.movex = player.movey = 0

