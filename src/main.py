from game_config import *
from ghosts import Ghost
from key_input import checkInput
import sys


def draw():

    screen.clear()
    screen.blit('colour_map', (0, 0))

    # draw player
    player.getImageAndDraw()
    drawScore()
    drawLives()

    # draw dots
    for d in dots:
        d.draw()

    # draw ghosts
    for g in ghosts:
        g.draw()

    if player.gameStatus == 2:
        drawCentreText("GAME OVER\nPress SPACE\nto try again")

    if player.gameStatus == 3:
        drawCentreText("YOU WON!\nPress SPACE\nto try again")

    if player.gameStatus == 1:
        drawCentreText("CAUGHT!\nPress SPACE\nto Continue")


def startFrightenedTimer():
    global isChasingMode

    isChasingMode = True

    for ghost in ghosts:
        ghost.setImage("ghost5")
        ghost.path = []

    if algorithm != 'GeneticAlgorithm':
        initGhostsAlgorithm(ghosts, player, 'Frightened')

    clock.schedule_unique(returnGhostsToNormal, 5.0)


def returnGhostsToNormal():
    global isChasingMode

    isChasingMode = False

    for ghost in ghosts:
        ghost.setImage("ghost" + str(ghost.index))
        ghost.path = []

    initGhostsAlgorithm(ghosts, player, algorithm)


def drawCentreText(msg):
    drawText(msg, (300, 300), 60)


def drawScore():
    drawText('Score: ' + str(player.score), (55, 340))


def drawLives():
    drawText('Lives left: ' + str(player.lives), (545, 340))


def drawText(msg, pos, fontsize=20):
    screen.draw.text(msg, center=pos, owidth=0.5, ocolor=(255, 255, 255), color=(255, 64, 0), fontsize=fontsize)


def update():
    global ghostMovement, isChasingMode, ghosts, ghostsInitialized

    # when player dies, reinitialize ghosts and wait for space press
    if player.gameStatus == 1:
        if not ghostsInitialized:
            ghosts = initGhosts()
            initGhostsAlgorithm(ghosts, player, algorithm)
            ghostsInitialized = True

        i = checkInput(player)
        if i == 1:
            player.restart()
            ghostsInitialized = False

    # when game is over or player won the game wait for space press
    if player.gameStatus == 2 or player.gameStatus == 3:
        i = checkInput(player)
        if i == 1:
            restartGame()

    # if player is human update game in every frame
    if player.getPlayerType() == 'human':
        player.update(dots, ghosts, isChasingMode)

    # calculate which dots are eaten
    for d in dots:
        if d.collidepoint((player.x, player.y)):
            if d.dotType == 1:
                sounds.pacman_eat.play()
                player.score += 10
                dots.remove(d)
            else:
                sounds.pacman_eat_big.play()
                player.score += 50
                dots.remove(d)
                startFrightenedTimer()
            break

    # if all dots are eaten player won game
    if len(dots) == 0:
        player.gameStatus = 3

    # check if player is caught
    if not isChasingMode:
        for ghost in ghosts:
            if player.gameStatus == 0:
                if player.caught(ghost, isChasingMode):
                    sounds.pacman_death.play()
                    player.lives -= 1
                    player.gameStatus = 1

    # if player lost all its lives game is over
    if player.lives == 0:
        player.gameStatus = 2
    else:
        ghostMovement += 1
        if ghostMovement == ITER:   # update in every ITER frame
            if player.gameStatus != 1:
                moveGhosts(ghosts)
            if player.getPlayerType() != 'human':
                player.update(dots, ghosts, isChasingMode)
            ghostMovement = 0

    # check if any ghost is eaten
    if isChasingMode:
        for ghost in ghosts:
            if player.caught(ghost, isChasingMode):
                sounds.pacman_eat_ghost.play()
                player.score += 200

                ghosts.remove(ghost)
                newGhost = Ghost(ghost.index, ghost.image,
                                 (270 + (ghost.index-1) * 20, 290), 0)
                initGhostAlgorithm(newGhost, player, algorithm)
                ghosts.append(newGhost)
                break


def restartGame():
    global dots, ghosts, ghostMovement

    player.onGameRestart()
    dots = initDots()
    ghosts = initGhosts()
    ghostMovement = 0
    initGhostsAlgorithm(ghosts, player, algorithm)


def init():
    music.play('background_music')
    music.set_volume(0.2)

    # depending on which algorithm user selected ghosts algorithm is being initialised
    player.setPlayerType(playerType)
    initGhostsAlgorithm(ghosts, player, algorithm)


algorithm = sys.argv[1]
playerType = sys.argv[2] # Choose agent :). It can be: human, rl, greedy, tree
init()
pgzrun.go()
