import pygame
import math
import time
from game.projectile import Projectile
from game.shooter import Shooter
from game.bird import Bird
from game.box import Box
from game.powerline import Powerline
from game.spark import Spark

projectiles = []
birds = []
boxes = []
powerlines = []
sparks = []

shooter = Shooter()


def main():
    pygame.init()
    background = (255,255,255)
    (width, height) = (640, 480)

    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("two birds, one stone")
    running = True

    # get some images
    shooterTex = pygame.image.load('data/gfx/shooter.png')
    projectileTex = pygame.image.load('data/gfx/rock.png')
    polesTex = pygame.image.load('data/gfx/poles.png')
    backgroundTex = pygame.image.load('data/gfx/background.png')
    birdTex = pygame.image.load('data/gfx/bird.png')
    birdTex_right = pygame.image.load('data/gfx/mbird_right.png')
    birdTex_left = pygame.image.load('data/gfx/mbird_left.png')
    boxTex = pygame.image.load('data/gfx/box.png')
    grassTex = pygame.image.load('data/gfx/grass.png')
    sparkTex_front = pygame.image.load('data/gfx/spark_front.png')
    sparkTex_back = pygame.image.load('data/gfx/spark_back.png')
    levelTextBorder = pygame.image.load('data/gfx/level_border.png')
    shotsTextBorder = pygame.image.load('data/gfx/shots_border.png')
    logoTex = pygame.image.load('data/gfx/logo.png')
    winOverlayTex = pygame.image.load('data/gfx/win_overlay.png')
    # get fonts
    font = pygame.font.Font('data/font/font.otf', 100)
    font_32 = pygame.font.Font('data/font/font.otf', 32)
    font_28 = pygame.font.Font('data/font/font.otf', 28)
    font_64 = pygame.font.Font('data/font/font.otf', 64)
    font_48 = pygame.font.Font('data/font/font.otf', 48)
    # get sounds
    bonkfx = pygame.mixer.Sound("data/sfx/bonk.wav")
    launchfx = pygame.mixer.Sound("data/sfx/launch.wav")
    killfx = pygame.mixer.Sound("data/sfx/kill.wav")
    losefx = pygame.mixer.Sound("data/sfx/lose.wav")
    winfx = pygame.mixer.Sound("data/sfx/win.wav")

    clock = pygame.time.Clock()

    currentLevel = 0
    shots = 0

    loadLevel(currentLevel)

    splashScreenTimer = 0
    pygame.mixer.Sound.play(winfx)
    while splashScreenTimer < 2:
        dt = clock.tick(60) / 1000
        splashScreenTimer += dt

        for event in pygame.event.get():
            # if the user clicks the button
            if event.type==pygame.QUIT:
                pygame.quit()
                pygame.sys.exit()

        display.fill((255, 255, 255))
        display.blit(backgroundTex, (0,0))
        startMessage = font_32.render("CREATED BY ME", True, (48, 93, 120))
        display.blit(startMessage, (display.get_width()/2 - startMessage.get_width()/2, display.get_height()/2 - startMessage.get_height()/2))
            
        # update display
        pygame.display.update()
        # wait for 10 seconds
        pygame.time.delay(10)
    
    titleScreen = True
    pygame.mixer.Sound.play(launchfx)
    # title screen
    while titleScreen:
        dt = clock.tick(60) / 1000
        # get the position of the mouse
        mouseX,mouseY = pygame.mouse.get_pos()  
        # getting the keys pressed
        clicked = False
        keys = pygame.key.get_pressed()
        # checking events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    titleScreen = False
                    pygame.mixer.Sound.play(launchfx)
            # if the player quits
            if event.type==pygame.QUIT:
                pygame.quit()
                pygame.sys.exit()

        display.fill((255, 255, 255))
        display.blit(backgroundTex, (0,0))
        display.blit(polesTex, (0,0))
        display.blit(grassTex, (0,0))
        display.blit(logoTex, (display.get_width()/2 - logoTex.get_width()/2, display.get_height()/2 - logoTex.get_height()/2 + math.sin(time.time()*5)*5 - 25)) 
        startMessage = font_32.render("SPACE TO START", True, (0, 0, 0))
        display.blit(startMessage, (display.get_width()/2 - startMessage.get_width()/2, 325))

        pygame.display.update()
        pygame.time.delay(10)

    while running:

        # calculate deltatime

        dt = clock.tick(60) / 1000

        shooter.setDirection(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if shooter.hasBullet:
                    pygame.mixer.Sound.play(launchfx)
                    shots += 1
                    shooter.hasBullet = False
                    projectiles.append(Projectile(shooter.position.x + shooter.width/2 - 29/2, shooter.position.y + 8))

        # update

        for projectile in projectiles:
            projectile.update(dt)
            if projectile.position.y + projectile.height < 0 or projectile.position.y > 480:
                projectiles.remove(projectile)
                if len(birds) is 0:
                    currentLevel += 1
                    reset(currentLevel) 
                    pygame.mixer.Sound.play(winfx)
                else:
                    reset(currentLevel)
                    pygame.mixer.Sound.play(losefx)
            if projectile.direction is -1 and checkCollisions(shooter.position.x, shooter.position.y, shooter.width, shooter.height, projectile.position.x, projectile.position.y, projectile.width, projectile.height):
                projectiles.remove(projectile)
                shooter.hasBullet = True


        for bird in birds:
            bird.update(dt)
            for projectile in projectiles:
                if checkCollisions(bird.position.x, bird.position.y, bird.width, bird.height, projectile.position.x, projectile.position.y, projectile.width, projectile.height):
                    birds.remove(bird)
                    pygame.mixer.Sound.play(killfx)

        if (currentLevel is 7) and len(birds) is 0:
            pygame.mixer.Sound.play(winfx)
            currentLevel += 1
            reset(currentLevel)
        
        for spark in sparks:
            spark.update(dt)
            for projectile in projectiles:
                if checkCollisions(spark.position.x, spark.position.y, spark.width, spark.height, projectile.position.x, projectile.position.y, projectile.width, projectile.height):
                    reset(currentLevel)
                    pygame.mixer.Sound.play(losefx)

        shooter.update(dt)

        for box in boxes:
            box.update(dt)
            for projectile in projectiles:
                if checkCollisions(box.position.x, box.position.y, box.width, box.height, projectile.position.x, projectile.position.y, projectile.width, projectile.height):
                    projectile.setDirection(-1)
                    pygame.mixer.Sound.play(bonkfx)


        # draw
    
        display.fill(background)
        display.blit(backgroundTex, (0,0))
        display.blit(grassTex, (0,0))

        for powerline in powerlines:
            pygame.draw.line(display, (0,0,0), (powerline.x1, powerline.y1), (powerline.x2, powerline.y2), 8)

        display.blit(polesTex, (0,0))

        for projectile in projectiles:
            display.blit(projectileTex, (projectile.position.x, projectile.position.y))

        for box in boxes:
            display.blit(boxTex, (box.position.x, box.position.y))

        for bird in birds:
            if (bird.direction == 1):
                display.blit(birdTex_right, (bird.position.x, bird.position.y))
            elif (bird.direction == -1):
                display.blit(birdTex_left, (bird.position.x, bird.position.y))  
            else:  
                display.blit(birdTex, (bird.position.x, bird.position.y))

        sparkSize = (int)(abs(math.sin(time.time()*5)*5)*5)
        sparkSize2 = (int)(abs(math.sin(time.time()*5 + 10)*5)*5)
        newSparkTex_back = pygame.transform.scale(sparkTex_back, (sparkSize, sparkSize))
        newSparkTex_front = pygame.transform.scale(sparkTex_front, (sparkSize2, sparkSize2))
        
        for spark in sparks:
            if spark.position.x > 43 and spark.position.x + spark.width < 640 - 43:
                display.blit(newSparkTex_back, (spark.position.x - sparkSize/2 + 13.5, spark.position.y - sparkSize/2 + 13.5))
                display.blit(newSparkTex_front, (spark.position.x - sparkSize2/2 + 13.5, spark.position.y - sparkSize2/2 + 13.5))


        if shooter.hasBullet:
            display.blit(projectileTex, (shooter.position.x + shooter.width/2 - 29/2, shooter.position.y - 6)) 
        display.blit(shooterTex, (shooter.position.x, shooter.position.y))

        if not (currentLevel > 9):

            display.blit(shotsTextBorder, (5, 475 - 39))
            display.blit(levelTextBorder, (640 - 144 - 5, 475 - 39))
        
            levelText = font_28.render('LEVEL: ' + str(currentLevel + 1) + '/10', True, (0, 0, 0))
            display.blit(levelText, (640 - 144 + 5, 475 - 39 + 4))

            shotsText = font_28.render('SHOTS: ' + str(shots).zfill(3), True, (0, 0, 0))
            display.blit(shotsText, (15, 475 - 39 + 4))

        if currentLevel > 9:
            display.blit(winOverlayTex, (0, 0))
            winText = font_48.render('GOVERNMENT DESTROYED.', True, (255, 255, 255))
            display.blit(winText, (320 - winText.get_width()/2, 240 - winText.get_height() - 20))
            shotsText = font_32.render('SHOTS: ' + str(shots), True, (255, 255, 255))
            display.blit(shotsText, (320 - shotsText.get_width()/2, 240 - shotsText.get_height() + 20))


        pygame.display.flip()

def loadLevel(level):
    if level is 0: #first level
        birds.append(Bird(320 - 31/2, 150 - 58, False, 0, 0, 0))
        birds.append(Bird(320 - 31/2, 150 - 58 + 100, False, 0, 0, 0))
        powerlines.append(Powerline(30, 150, 610, 150))
        powerlines.append(Powerline(30, 250, 610, 250))
    if level is 1: #moving bird + normal bird
        birds.append(Bird(320 - 31/2 + 150, 250 - 58, False, 0, 0, 0))
        birds.append(Bird(320 - 31/2 - 200, 150 - 58, True, 400, 1, 70))
        powerlines.append(Powerline(30, 150, 610, 150))
        powerlines.append(Powerline(30, 250, 610, 250))
    if level is 2: #two moving birds
        birds.append(Bird(320 - 31/2 - 100, 100 - 58, True, 200, 1, 70))
        birds.append(Bird(320 - 31/2 + 100, 100 - 58 + 150, True, 200, -1, 70))
        powerlines.append(Powerline(30, 100, 610, 100))
        powerlines.append(Powerline(30, 250, 610, 250))
    if level is 3: #level that introduces boxes
        birds.append(Bird(320 - 31/2 - 100, 100 - 58, False, 0, 0, 0))
        birds.append(Bird(320 - 31/2 + 100, 100 - 58 + 150, False, 0, 0, 0))
        boxes.append(Box(320 - 64/2 + 100, 100 - 32))
        powerlines.append(Powerline(30, 100, 610, 100))
        powerlines.append(Powerline(30, 250, 610, 250))
    if level is 4: #boxes + moving birds
        birds.append(Bird(320 - 31/2 - 250, 200 - 58, True, 100, 1, 70))
        birds.append(Bird(320 - 31/2 - 150, 300 - 58, True, 100, -1, 70))
        boxes.append(Box(320 - 64/2 - 200, 100 - 32))

        birds.append(Bird(320 - 31/2 - 250 + 200, 200 - 58, True, 100, 1, 70))
        birds.append(Bird(320 - 31/2 - 150 + 200, 300 - 58, True, 100, -1, 70))

        birds.append(Bird(320 - 31/2 - 250 + 400, 200 - 58, True, 100, 1, 70))
        birds.append(Bird(320 - 31/2 - 150 + 400, 300 - 58, True, 100, -1, 70))
        boxes.append(Box(320 - 64/2 - 200 + 400, 100 - 32))

        powerlines.append(Powerline(30, 100, 610, 100))
        powerlines.append(Powerline(30, 200, 610, 200))
        powerlines.append(Powerline(30, 300, 610, 300))
    if level is 5: #intro to sparks
        birds.append(Bird(320 - 31/2, 150 - 58, False, 0, 0, 0))
        sparks.append(Spark(320 - 14 - 50, 250 - 14, True, 114, 1, 50))
        powerlines.append(Powerline(30, 150, 610, 150))
        powerlines.append(Powerline(30, 250, 610, 250))
    if level is 6: #2 sparks + moving bird
        birds.append(Bird(320 - 31/2 - 50, 150 - 58, True, 114, 1, 50))
        sparks.append(Spark(320 - 14 - 28 - 50, 250 - 14, True, 114, 1, 50))
        sparks.append(Spark(320 - 14, 250 - 14, True, 114, 1, 50))
        powerlines.append(Powerline(30, 150, 610, 150))
        powerlines.append(Powerline(30, 250, 610, 250))
    if level is 7: #sparks + box
        birds.append(Bird(320 - 31/2 - 250, 275 - 58, True, 320 + 157, 1, 90))
        sparks.append(Spark(320 - 21 - 250, 300 - 14, True, 320 + 157, 1, 90))
        sparks.append(Spark(320 - 21 - 250 + 28, 300 - 14, True, 320 + 157, 1, 90))
        sparks.append(Spark(320 - 21 - 250 + 56, 300 - 14, True, 320 + 157, 1, 90))
        sparks.append(Spark(320 - 21 - 250 - 28, 300 - 14, True, 320 + 157, 1, 90))
        boxes.append(Box(320 - 64/2, 100 - 32))

        powerlines.append(Powerline(30, 100, 610, 100))
        powerlines.append(Powerline(30, 275, 610, 275))
        powerlines.append(Powerline(30, 300, 610, 300))
    if level is 8: #final level
        birds.append(Bird(320 - 31/2 - 175, 200 - 58, False, 0, 0, 0))
        birds.append(Bird(320 - 31/2 - 87.5, 200 - 58, False, 0, 0, 0))
        birds.append(Bird(320 - 31/2, 100 - 58, False, 0, 0, 0))
        birds.append(Bird(320 - 31/2 + 87.5, 200 - 58, False, 0, 0, 0))
        birds.append(Bird(320 - 31/2 + 175, 200 - 58, False, 0, 0, 0))

        boxes.append(Box(320 - 32 - 175, 100 - 32))
        boxes.append(Box(320 - 32 - 87.5, 100 - 32))
        boxes.append(Box(320 - 32 + 87.5, 100 - 32))
        boxes.append(Box(320 - 32 + 175, 100 - 32))

        sparks.append(Spark(320 - 14 - 50 - 200 - 450, 300 - 14, True, 414, 1, 50))
        
        sparks.append(Spark(320 - 14 - 50 - 200 - 300, 300 - 14, True, 414, 1, 50))
        
        sparks.append(Spark(320 - 14 - 50 - 200 - 150, 300 - 14, True, 414, 1, 50))
        
        sparks.append(Spark(320 - 14 - 50 - 200, 300 - 14, True, 414, 1, 50))
        sparks.append(Spark(320 - 14 - 200 + 100, 300 - 14, True, 414, 1, 50))

        sparks.append(Spark(320 - 14 - 200 + 100 + 150, 300 - 14, True, 414, 1, 50))

        sparks.append(Spark(320 - 14 - 200 + 100 + 300, 300 - 14, True, 414, 1, 50))
        
        powerlines.append(Powerline(30, 100, 610, 100))
        powerlines.append(Powerline(30, 200, 610, 200))
        powerlines.append(Powerline(30, 300, 610, 300))
    if level is 9: # fun final level
        birds.append(Bird(320 - 31/2 + 100, 225 - 58, True, 400, -1, 25))
        birds.append(Bird(320 - 31/2 - 100, 300 - 58, True, 400, 1, 25))
        birds.append(Bird(320 - 31/2 + 200, 75 - 58, True, 400, -1, 50))
        birds.append(Bird(320 - 31/2 - 200, 150 - 58, True, 400, 1, 50))

        powerlines.append(Powerline(30, 75, 610, 75))
        powerlines.append(Powerline(30, 150, 610, 150))
        powerlines.append(Powerline(30, 225, 610, 225))
        powerlines.append(Powerline(30, 300, 610, 300))
    if level > 9:
        return

def reset(level):
    if level > 9:
        return
    projectiles.clear()
    birds.clear()
    boxes.clear()
    sparks.clear()
    powerlines.clear()
    loadLevel(level)
    shooter.reset()

def checkCollisions(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
    return (a_x + a_width > b_x) and (a_x < b_x + b_width) and (a_y + a_height > b_y) and (a_y < b_y + b_height)

if __name__ == "__main__":
    main()