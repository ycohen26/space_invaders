import random
import math

import pygame
from pygame import mixer

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1000, 667))

# background
background = pygame.image.load('background.jpg')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invadors")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('player.png')
playerX = 500
playerY = 540
playerX_change = 0

# enemy 1
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = (random.randint(6, 10))

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy_4.png'))
    enemyX.append(random.randint(0, 936))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# missile 1

# ready = can't see missile
# fire = the missile is moving

missileImg = pygame.image.load('missile.png')
missileX = 0
missileY = 540
missileX_change = 0
missileY_change = 7
missile_state = "ready"

# explosion
explosionImg = pygame.image.load('boom.png')

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# game over text
score_value = 0
over_font = pygame.font.Font('freesansbold.ttf', 64)

textx = 10
texty = 10

def show_score(x,y):
    score = font.render("Score :" +str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))
    
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (310, 300))

def player(x,y):
    screen.blit(playerImg, (x, y))


def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImg, (x + 16, y + 10))
    
def isCollision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt((math.pow(enemyX - missileX,2)) + (math.pow(enemyY - missileY,2)))
    if distance <= 27:
        return True

def missle_explode(x,y):
    screen.blit(explosionImg, (x,y))

# game loop
running = True
while running:
  
    # RGB 
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check if right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if missile_state is "ready":
                    missle_sound = mixer.Sound('laser.wav')
                    missle_sound.play()
                    missileX = playerX
                    fire_missile(missileX, missileY)
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0        

    # keep spaceship in bounds
    playerX += playerX_change
    
    if playerX <= 0:
        playerX = 0
    elif playerX >= 936:
        playerX = 936

    
    # enemy movement
    for i in range(num_of_enemies):
      
        # game over
        
        if enemyY[i] > 485:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # keep enemy in bounds
        enemyX[i] += enemyX_change[i]
        
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 936:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        

        # collision
        colission = isCollision(enemyX[i], enemyY[i], missileX, missileY)
        if colission:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            missle_explode(enemyX[i], enemyY[i])
            missileY = 540
            missile_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 936)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)    
      
            
    # missile movement
    if missileY <=0:
        missileY = 540
        missile_state = "ready"

    if missile_state is "fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change
        
        
    player(playerX, playerY)
    show_score(textx, texty)
    pygame.display.update()