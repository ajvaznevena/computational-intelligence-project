from algorithms.rl.reinforcement_learning import Environment
from grid.get_grid import get_grid

import numpy as np


def stateTransformer(player, dots, ghosts, isChasingMode):

    state = np.array(get_grid(), copy=True)

    Environment.mapPlayerOnGrid(player, state)
    Environment.mapDotsOnGrid(dots, state)
    Environment.mapGhostsOnGrid(ghosts, state, isChasingMode)

    return state
