from pgzero.builtins import Actor
from maps import checkDotPoint


class Dot(Actor):

    def __init__(self, t, img, pos):
        super().__init__(img, pos)
        self.dotType = t


def initDots():
    dots = []

    for i in range(30):
        for j in range(29):
            dotPos = (10 + i * 20, 10 + j * 20)

            color = checkDotPoint(dotPos)

            if color == 1:
                dot = Dot(1, "dot", dotPos)
                dots.append(dot)

            elif color == 2:
                dot = Dot(2, "power", dotPos)
                dots.append(dot)

    return dots
