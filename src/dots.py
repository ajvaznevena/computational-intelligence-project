from game_config import *


def initDots():
    for i in range(30):
        for j in range(29):
            color = maps.checkDotPoint(10 + i * 20, 10 + j * 20)

            if color == 1:
                dot = Actor("dot", (10 + i * 20, 10 + j * 20))
                dot.type = 1
                dots.append(dot)

            elif color == 2:
                dot = Actor("power", (10 + i * 20, 10 + j * 20))
                dot.type = 2
                dots.append(dot)