from algorithms.agents.grid_config import *

from pygame import image, Color


class Dot:

    def __init__(self, t, i, j):
        self.dotType = t
        self.i = i
        self.j = j


def initDots():
    dotImage = image.load('images/dot_map.png')

    dots = []

    for i in range(int(WIDTH / CELL_SIZE)):
        for j in range(int(HEIGHT / CELL_SIZE)):
            dotPos = (int(CELL_SIZE / 2 + i * CELL_SIZE), int(CELL_SIZE / 2 + j * CELL_SIZE))

            if dotImage.get_at(dotPos) == Color('black'):
                dot = Dot(1, j, i)
                dots.append(dot)

            elif dotImage.get_at(dotPos) == Color('red'):
                dot = Dot(2, j, i)
                dots.append(dot)

    return dots
