from game_config import *
from algorithms.a_star import AStar
from algorithms.genetic_algorithm import GeneticAlgorithm


def draw():

    screen.clear()
    screen.blit('colour_map', (0, 0))

    # draw player
    player.getImageAndDraw()
    drawScore()

    # draw dots
    for d in dots:
        d.draw()

    # draw ghosts
    for g in ghosts:
        g.draw()

    if player.gameStatus == 2:
        drawCentreText("GAME OVER")

    if player.gameStatus == 3:
        drawCentreText("YOU WON!")

    if player.gameStatus == 1:
        drawCentreText("CAUGHT!\nPress SPACE\nto Continue")


def startTimer():
    global timer

    timer = time.time()


def drawCentreText(msg):
    screen.draw.text(msg, center=(300, 300), owidth=0.5,
                     ocolor=(255, 255, 255), color=(255, 64, 0), fontsize=60)


def drawScore():
    screen.draw.text('Score: ' + str(player.score), center=(55, 340), owidth=0.5,
                     ocolor=(255, 255, 255), color=(255, 64, 0), fontsize=30)


def update():
    global ghostMovement  # to change global variable this statement is needed
    global isChasingMode
    global timer

    player.update()

    # calculating passed time if in chasing mode
    if isChasingMode and time.time() - timer > SECONDS:
        timer = 0
        isChasingMode = False
        for ghost in ghosts:
            ghost.setImage("ghost" + str(ghost.index))

    # calculating dots
    for d in dots:
        if d.collidepoint((player.x, player.y)):
            sounds.pacman_eat.play()
            if d.dotType == 1:
                player.score += 10
                dots.remove(d)
                break
            else:
                player.score += 20
                dots.remove(d)
                isChasingMode = True
                startTimer()

    if len(dots) == 0:
        player.gameStatus = 3

    if not isChasingMode:
        for ghost in ghosts:
            if player.gameStatus == 0:
                if player.caught(ghost, isChasingMode):
                    player.lives -= 1
                    player.gameStatus = 1

    else:
        for ghost in ghosts:
            ghost.setImage("ghost5")

            if player.caught(ghost, isChasingMode):
                sounds.pacman_eat_ghost.play()
                ghost.x = 290
                ghost.y = 290
                ghost.path = []

    if player.lives == 0:
        player.gameStatus = 2
        sounds.pacman_death.play()

    ghostMovement += 1
    if ghostMovement == ITER:
        if player.gameStatus != 1:
            moveGhosts(ghosts)
        ghostMovement = 0


def init():
    music.play('background_music')
    music.set_volume(0.2)

    # depending on which algorithm user selected ghosts algorithm is being initialised
    for g in ghosts:

        if algorithm == 'A*':
            g.setAlgorithm(AStar(g))

        elif algorithm == 'gen':
            g.setAlgorithm(GeneticAlgorithm(g))


# TODO da ne smara svaki put, za sad imamo samo A* pa ne mora da se unosi :D
algorithm = 'A*'
# algorithm = 'gen'
# algorithm = input("Enter which algorithm to use for ghosts: ")

init()
pgzrun.go()
