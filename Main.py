# imported modules
import pygame, sys, random


def drawFloor():
    screen.blit(floorSurface, (floorXPos, 900))
    screen.blit(floorSurface, (floorXPos + 576, 900))


def createPipe():
    randomPipePos = random.choice(pipeHeight)
    bottomPipe = pipeSurface.get_rect(midtop=(700, randomPipePos))
    topPipe = pipeSurface.get_rect(midbottom=(700, randomPipePos - 300))
    return bottomPipe, topPipe


def movePipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipeSurface, pipe)
        else:
            flipPipe = pygame.transform.flip(pipeSurface, False, True)
            screen.blit(flipPipe, pipe)


def checkCollision(pipes):
    for pipe in pipes:
        if birdRect.colliderect(pipe):
            return False

    if birdRect.top <= -100 or birdRect.bottom >= 900:
        return False

    return True


def rotateBird(bird):
    newBird = pygame.transform.rotozoom(bird, -birdMovement * 3, 1)
    return newBird

def birdAnimation():
    newBird = birdFrames[birdIndex]
    newBirdRect = newBird.get_rect(center = (100, birdRect.centery))
    return newBird, newBirdRect

def scoreDisplay(gameState):
    if gameState == 'mainGame':
        score_surface = gameFont.render(str(int(score)), True, (255, 255, 255))
        scoreRect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, scoreRect)
    if gameState == 'gameOver':
        score_surface = gameFont.render(f'Score: {int(score)}', True, (255, 255, 255))
        scoreRect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, scoreRect)

        Highscore_surface = gameFont.render(str(int(score)), True, (255, 255, 255))
        HighscoreRect = Highscore_surface.get_rect(center=(288, 850))
        screen.blit(Highscore_surface, HighscoreRect)

# initialize pygame/screen
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
gameFont = pygame.font.Font('Font-file/04B_19.TTF', 40)

gravity = 0.25
birdMovement = 0
gameActive = True
score = 0
highScore = 0

bgSurface = pygame.image.load('game-images/background-day.png').convert()
bgSurface = pygame.transform.scale2x(bgSurface)

floorSurface = pygame.image.load('game-images/base.png').convert()
floorSurface = pygame.transform.scale2x(floorSurface)
floorXPos = 0

birdDownFlap = pygame.transform.scale2x(pygame.image.load('game-images/bluebird-downflap.png').convert_alpha())
birdMidFlap = pygame.transform.scale2x(pygame.image.load('game-images/bluebird-midflap.png').convert_alpha())
birdUpFlap = pygame.transform.scale2x(pygame.image.load('game-images/bluebird-upflap.png').convert_alpha())
birdFrames = [birdDownFlap, birdMidFlap, birdUpFlap]
birdIndex = 0
birdSurface = birdFrames[birdIndex]
birdRect = birdSurface.get_rect(center = (100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)



pipeSurface = pygame.image.load('game-images/pipe-green.png')
pipeSurface = pygame.transform.scale2x(pipeSurface)
pipeList = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipeHeight = [400, 600, 800]

# game loop
while True:
    for event in pygame.event.get():
        # close screen
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameActive:
                birdMovement = 0
                birdMovement -= 12
            if event.key == pygame.K_SPACE and gameActive == False:
                gameActive = True
                pipeList.clear()
                birdRect.center = (100, 512)
                birdMovement = 0

        if event.type == SPAWNPIPE:
            pipeList.extend(createPipe())

        if event.type == BIRDFLAP:
            if birdIndex < 2:
                birdIndex += 1
            else:
                birdIndex = 0
            birdSurface,birdRect = birdAnimation()

    screen.blit(bgSurface, (0, 0))

    if gameActive:
        birdMovement += gravity
        rotatedBird = rotateBird(birdSurface)
        birdRect.centery += birdMovement
        screen.blit(rotatedBird, birdRect)
        gameActive = checkCollision(pipeList)

        pipeList = movePipe(pipeList)
        drawPipes(pipeList)
        score += 0.01
        scoreDisplay('mainGame')
    else:
        scoreDisplay('gameOver')

    floorXPos -= 1

    drawFloor()
    if floorXPos <= -576:
        floorXPos = 0

    pygame.display.update()
    clock.tick(120)
