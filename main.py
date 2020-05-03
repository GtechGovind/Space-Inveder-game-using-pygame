import math
import random

import pygame
from pygame import mixer


# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')

# Sound
def startMusic():
    mixer.music.load("background.mp3")
    mixer.music.play(-1)

startMusic()

def stopMusic():
    pygame.mixer.music.stop()

# Menu_background
menuBackgroundImg = pygame.image.load('trans.png')

# Welcome Condition defination 
welcomeCondition = True

def welcomeScreen():
    welcomeFont = pygame.font.Font('freesansbold.ttf', 35)
    welcomeDescription_Font = pygame.font.Font('freesansbold.ttf', 22)
    welcomeText = welcomeFont.render("SPACE INVEDERS", True, (255, 69, 0))
    welcomeDescription_Text = welcomeDescription_Font.render("PRESS \"SPACE\" TO PLAY", True, (254, 231, 21))
    screen.blit(menuBackgroundImg, (200, 50))
    screen.blit(welcomeText, (250, 100))
    screen.blit(welcomeDescription_Text, (260, 155))

    




# Game Loop
running = True
while running == True:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    if welcomeCondition == True:
        # Welcome Screen
        welcomeScreen()
        # Welcome Page Image load
        base = pygame.image.load('base.png')
        screen.blit(base, (0, 250))
        for event in pygame.event.get():
            
            # Exit control
            if event.type == pygame.QUIT:
                running = False

            # Game start Condition
            if event.type == pygame.KEYDOWN:
                startMusic()
                welcomeCondition = False
                gameRunning = True
    else:

        # Space Invaders Game Begins

        # Variable Definations

        # Player
        playerImg = pygame.image.load('player.png')
        playerX = 370
        playerY = 480
        playerX_change = 0

        # Enemy
        enemyImg = []
        enemyX = []
        enemyY = []
        enemyX_change = []
        enemyY_change = []
        num_of_enemies = 6

        for i in range(num_of_enemies):
            enemyImg.append(pygame.image.load('enemy.png'))
            enemyX.append(random.randint(0, 736))
            enemyY.append(random.randint(50, 150))
            enemyX_change.append(4)
            enemyY_change.append(40)

        # Bullet

        # Ready - You can't see the bullet on the screen
        # Fire - The bullet is currently moving

        bulletImg = pygame.image.load('bullet.png')
        bulletX = 0
        bulletY = 480
        bulletX_change = 0
        bulletY_change = 10
        bullet_state = "ready"

        # Function Definations

        def player(x, y):
            screen.blit(playerImg, (x, y))
        
        def enemy(x, y, i):
            screen.blit(enemyImg[i], (x, y))

        
        def fire_bullet(x, y):
            global bullet_state
            bullet_state = "fire"
            screen.blit(bulletImg, (x + 16, y + 10))

        def isCollision(enemyX, enemyY, bulletX, bulletY):
            distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
            if distance < 27:
                return True
            else:
                return False

        score_value = 0
        font = pygame.font.Font('freesansbold.ttf', 32)

        def show_score():
            global score
            score_bord = font.render("[ " + str(score_value) + " ]", True, (254 , 231, 21))
            score = font.render("SCORE : " + str(score_value), True, (254 , 231, 21))
            if gameRunning == True:
                screen.blit(score_bord, (10, 10))
            else:
                pass

        def gameOver():
            stopMusic()
            # Refrshing the Screen
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            screen.blit(menuBackgroundImg, (200, 100))
            over_font = pygame.font.Font('freesansbold.ttf', 55)
            over_text = over_font.render("GAME OVER", True, (254 , 231, 21))
            screen.blit(over_text, (230, 150))
            screen.blit(score, (320, 220))
        
        # Game Control Loop
        while gameRunning == True:
            # Refrshing the Screen
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))
            
            # Exit control for Game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameRunning = False
                    welcomeCondition = True

                # Player Movment
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        playerX_change = -5

                    if event.key == pygame.K_RIGHT:
                        playerX_change = 5

                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            bulletSound = mixer.Sound("laser.wav")
                            bulletSound.play()
                            # Get the current x cordinate of the spaceship
                            bulletX = playerX

                            fire_bullet(bulletX, bulletY)


                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            playerX_change = 0
            
            # Player movement boundry condition
            playerX += playerX_change
            if playerX <= 0:
                playerX = 0
            elif playerX >= 736:
                playerX = 736

            # Enemy Movement
            for i in range(num_of_enemies):

                # Game Over
                if enemyY[i] > 300:
                    for j in range(num_of_enemies):
                        enemyY[j] = 2000
                    gameOver()
                    break

                enemyX[i] += enemyX_change[i]
    
                if enemyX[i] <= 0:
                    enemyX_change[i] = 4
                    enemyY[i] += enemyY_change[i]

                elif enemyX[i] >= 736:
                    enemyX_change[i] = -4
                    enemyY[i] += enemyY_change[i]

                enemy(enemyX[i], enemyY[i], i)

                # Collision
                collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision:
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                    bulletY = 480
                    bullet_state = "ready"
                    score_value += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)
                
        # Bullet Movement
            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"
            
            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change
            
            
            player(playerX, playerY)
            show_score()
            pygame.display.update()

    if welcomeCondition == True: 
        pygame.display.update()
    else:
        continue
