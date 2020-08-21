from pygame import mixer
import math
import random
import pygame

pygame.init()
screen=pygame.display.set_mode((800,600))

mixer.music.load("bgm.mp3")
mixer.music.play(-1)

running=True

pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("alien.png")
pygame.display.set_icon(icon)

bullet=pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletY_change=10
bullet_state="ready"

background=pygame.image.load("space.jpg")
playerImg=pygame.image.load("space-invaders.png")
playerX=370
playerY=480
playerX_change=5

enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
no_of_enemies=6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("pacman.png"))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

def player(x,y):
    screen.blit(playerImg,(x,y))

score_value=0
font=pygame.font.Font("freesansbold.ttf",32)

textx=7
texty=7

def showscore(x,y):
    score=font.render("Score : "+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def firebullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bullet,(x+16,y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance<=27:
        return True
    return False

def gameover():
    score=font.render("Game Over",True,(255,255,255))
    screen.blit(score,(320,250))

while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-5
            if event.key==pygame.K_RIGHT:
                playerX_change=5
            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    bulletX=playerX
                    firebullet(bulletX,bulletY)

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0

    playerX+=playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736

    for i in range(no_of_enemies):
        if enemyY[i]>440:
            for j in range(no_of_enemies):
                enemyY[j]=2000
            gameover()
            break
        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-4
            enemyY[i]+=enemyY_change[i]

        collision=iscollision(enemyX[i],enemyY[i],bulletX,bulletY)

        if collision:
            bulletY=480
            bullet_state="ready"
            score_value+=1
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(0,150)
        
        enemy(enemyX[i],enemyY[i],i)

    if bullet_state=="fire":
        firebullet(bulletX,bulletY)
        bulletY-=bulletY_change

    
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"

    player(playerX,playerY)
    showscore(textx,texty)
    pygame.display.update()