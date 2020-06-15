from algorithms.agents.greedy_agent import GreedyAgent
from algorithms.agents.tree_agent import TreeAgent
from key_input import checkInput, playerMove
from maps import checkMovePoint
# from algorithms.agents.dqn import Agent
from game_state import stateTransformer
from grid.get_grid import get_grid

from pgzero.builtins import Actor
from pgzero.animation import animate
import numpy as np


class Player(Actor):

    def __init__(self, img, type):
        super().__init__(img)

        self.pos = 290, 490
        self.lives = 3
        self.score = 0
        self.gameStatus = 0
        self.angle = 0
        self.movex = 0
        self.movey = 0
        self.inputEnabled = True

        self.eatAnimation = 0
        self.died = False

        self.type = type

        if type == 'rl':
            self.agent = Agent(np.array(get_grid()).shape, 4)
        elif type == 'greedy':
            self.agent = GreedyAgent()
        elif type == 'tree':
            self.agent = TreeAgent()
        else:
            self.agent = None   # human is playing game

    def getPlayerType(self):
        return self.type

    def inputEnable(self):
        self.movex = self.movey = 0
        self.inputEnabled = True

    def getImageAndDraw(self):
        if self.gameStatus != 0:
            return

        angle = self.angle

        self.eatAnimation = (self.eatAnimation + 1) % 10

        # if player died stop animation
        if self.died:
            self.draw()
            return

        if self.eatAnimation < 6 and (self.movex != 0 or self.movey != 0):
            if angle != 180:
                self.image = "pacman"
            else:
                self.image = "pacman_r"
        else:
            if angle != 180:
                self.image = "pacman_eat"
            else:
                self.image = "pacman_eat_r"     # only going left is not possible using first image, due to rotation

        self.angle = angle  # rotate image
        self.draw()

    def caught(self, ghost, chasing):
        if self.collidepoint(ghost.pos) and not chasing:
            self.died = True

        return self.collidepoint(ghost.pos)

    def restart(self):
        self.pos = 290, 490
        self.gameStatus = 0
        self.angle = 0
        self.movex = 0
        self.movey = 0
        self.eatAnimation = 0
        self.died = False

        if self.type == 'greedy':
            self.agent.path = []
        elif self.type == 'tree':
            self.agent = TreeAgent()

    def onGameRestart(self):
        self.restart()
        self.lives = 3
        self.score = 0
        self.inputEnabled = True

    @staticmethod
    def mapActionIndexToString(action):
        if action == 0: return 'UP'
        elif action == 1: return 'DOWN'
        elif action == 2: return 'LEFT'
        elif action == 3: return 'RIGHT'
        elif action == 4: return 'STAY'

    def update(self, dots, ghosts, isChasingMode):

        if self.gameStatus == 0:  # player is moving
            if self.inputEnabled:
                if self.type == 'human':
                    checkInput(self)

                elif self.type == 'rl':
                    state = stateTransformer(self, dots, ghosts, isChasingMode)
                    predicted_action = self.agent.act_best_action(state)

                    print(f'Action: {Player.mapActionIndexToString(predicted_action)}')
                    playerMove(self, predicted_action)

                elif self.type == 'greedy':
                    predicted_action = self.agent.actBestAction(self, dots)

                    print(f'Action: {Player.mapActionIndexToString(predicted_action)}')
                    playerMove(self, predicted_action)

                elif self.type == 'tree':
                    predicted_action = self.agent.actBestAction(self, ghosts, dots, isChasingMode)

                    print(f'Action: {Player.mapActionIndexToString(predicted_action)}')
                    playerMove(self, predicted_action)

                checkMovePoint(self)

                if self.movex or self.movey:
                    self.inputEnabled = False
                    animate(self, pos=(self.x + self.movex, self.y + self.movey),
                            duration=1 / 3, tween='linear', on_finished=self.inputEnable)
