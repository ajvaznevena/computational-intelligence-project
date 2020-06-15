from pgzero.builtins import Actor
from maps import checkDotPoint

from game_constants import WIDTH, HEIGHT, CELL_SIZE


class Dot(Actor):

    def __init__(self, t, img, pos, i, j):
        super().__init__(img, pos)
        self.dotType = t
        self.i = i
        self.j = j


def initDots():
    """ Initializes dots based on dot map image """

    dots = []

    for i in range(int(WIDTH / CELL_SIZE)):
        for j in range(int(HEIGHT / CELL_SIZE)):

            # center dot on cell
            dotPos = (CELL_SIZE / 2 + i * CELL_SIZE, CELL_SIZE / 2 + j * CELL_SIZE)

            color = checkDotPoint(dotPos)

            if color == 1:  # small dot
                dot = Dot(1, "dot", dotPos, j, i)
                dots.append(dot)

            elif color == 2:    # bit dot
                dot = Dot(2, "power", dotPos, j, i)
                dots.append(dot)

    return dots
