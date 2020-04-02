from player import *
from ghosts import *
from dots import *


def draw():
    global isInitialized
    global isChasingMode

    screen.clear()
    screen.blit('colour_map', (0, 0))

    # draw player
    getPlayerImage()
    player.draw()

    # drawing dots
    for d in dots:
        if d.collidepoint((player.x, player.y)):
            sounds.pacman_eat.play()
            if d.type == 1:
                player.score += 10
                dots.remove(d)
                break
            else:
                player.score += 20
                dots.remove(d)
                isChasingMode = True
                if not isInitialized:
                    initRunningGhosts()
                isInitialized = True
                measureTime()

    for d in dots:
        d.draw()

    if len(dots) == 0:
        player.gameStatus = 3

    # drawing ghosts
    for g in ghosts:
        g.draw()
        if player.gameStatus == 0:
            if caught(g):
                if not isChasingMode:
                    player.gameStatus = 1

    # drawing running ghosts
    for g in runGhosts:
        if player.collidepoint((g.x, g.y)):
            sounds.pacman_eat_ghost.play()
            g.x = 290
            g.y = 290
        g.draw()

    if player.lives == 0:
        player.gameStatus = 2

    if player.gameStatus == 2:
        drawCentreText("GAME OVER")

    if player.gameStatus == 3:
        drawCentreText("YOU WON")

    if player.gameStatus == 1:
        drawCentreText("CAUGHT!\nPress Space\nto Continue")
        sounds.pacman_death.play()


def measureTime():
    thread1 = threading.Thread(target=timer)
    thread1.start()


def timer():
    global isChasingMode
    for i in range(SECONDS):
        time.sleep(1)
    isChasingMode = False


def drawCentreText(msg):
    screen.draw.text(msg, center=(300, 300), owidth=0.5, ocolor=(255, 255, 255), color=(255, 64, 0), fontsize=60)


def update():
    global ghostMovement    # to change global variable this statement is needed

    if player.gameStatus == 0:  # player is moving
        if player.inputEnabled:
            key_input.checkInput(player)
            maps.checkMovePoint(player)

            if player.movex or player.movey:
                player.inputEnabled = False
                animate(player, pos=(player.x + player.movex, player.y + player.movey),
                        duration=1 / SPEED, tween='linear', on_finished=inputEnable)

    elif player.gameStatus == 1:  # player caught
        i = key_input.checkInput(player)

        if i == 1:
            player.gameStatus = 0
            player.x = 290
            player.y = 490
            player.angle = 0

        return

    elif player.gameStatus == 2:
        i = key_input.checkInput(player)

        if i == 1:
            print("GAME OVER")
            sys.exit(0)

    ghostMovement += 1
    if ghostMovement == ITER:
        if player.gameStatus != 1 and isChasingMode == False:
            moveGhosts()
        else:
            moveRunningGhosts()
        ghostMovement = 0


def init(alg):
    music.play('background_music')
    music.set_volume(0.3)

    initPlayer()
    initDots()
    initGhosts(alg)


# TODO da ne smara svaki put, za sad imamo samo A* pa ne mora da se unosi :D
algorithm = 'A*'
# algorithm = 'gen'
# algorithm = input("Enter which algorithm to use for ghosts: ")
init(algorithm)
pgzrun.go()
