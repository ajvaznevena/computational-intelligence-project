from pgzero.builtins import Actor


class Ghost(Actor):

    def __init__(self, index, img, pos):
        super().__init__(img, pos)
        self.index = index
        self.path = []
        self.algorithm = None

    def setAlgorithm(self, algorithm):
        self.algorithm = algorithm

    def setImage(self, image):
        self.image = image


def initGhosts():
    ghosts = []

    for i in range(1, 5, 1):
        ghost = Ghost(i, "ghost" + str(i), (270 + (i-1) * 20, 290))

        if i == 3:
            ghost.path.append("n1_1")
        ghosts.append(ghost)

    return ghosts


def moveGhosts(ghosts):
    for ghosts in ghosts:
        # because all algorithms implement the same interface we can call getNextStep
        node = ghosts.algorithm.getNextStep()
        if node is None:
            return

        index = node.find('_')
        ghosts.x = int(node[index + 1:]) * 20 + 10
        ghosts.y = int(node[1:index]) * 20 + 10
