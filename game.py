"""
Corona Annilation

"""
#Import
import math
import random
import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('19682.jpg')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Corona Annilation")
icon = pygame.image.load('no.png')
pygame.display.set_icon(icon)

# Doctor and Details
doctorImg = pygame.image.load('doctor.png')
doctorX = 370
doctorY = 480
doctorX_change = 0

# victim and Dtails
victimImg = []
victimX = []
victimY = []
victimX_change = []
victimY_change = []
num_of_victim = 6


for i in range(num_of_victim):
    ani_1 = pygame.image.load('corona.png')
    victimImg.append(ani_1)    
    victimX.append(random.randint(0, 736))
    victimY.append(random.randint(50, 150))
    victimX_change.append(4)
    victimY_change.append(40)

ani_2 = pygame.image.load('pill.png')
pillImg = ani_2
pillX = 0
pillY = 480
pillX_change = 0
pillY_change = 10
pill_state = "ready"

# Score Calculation
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 40
testY = 40

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Kills: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("CORONA GONE !", True, (255, 255, 255))
    
    screen.blit(over_text, (140, 200))


def doctor(x, y):
    screen.blit(doctorImg, (x, y))


def victim(x, y, i):
    screen.blit(victimImg[i], (x, y))


def fire_pill(x, y):
    global pill_state
    pill_state = "fire"
    screen.blit(pillImg, (x + 16, y + 10))


def isCollision(victimX, victimY, pillX, pillY):
    distance = math.sqrt(math.pow(victimX - pillX, 2) + (math.pow(victimY - pillY, 2)))
    


#def show_go_screen(self):
        # game over/continue
#        if not self.running:
#           return

#       bg = pg.image.load("background1.png")
#       self.screen.blit(bg,(0,0))



#     self.draw_text("Press space bar to play again", 22, WHITE, WIDTH / 2, HEIGHT * 7 / 8) HEIGHT / 2 + 40)



# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                doctorX_change = -5
            if event.key == pygame.K_RIGHT:
                doctorX_change = 5
            if event.key == pygame.K_SPACE:
                if pill_state == "ready":
                    pillSound = mixer.Sound("laser.wav")
                    pillSound.play()
                    # Get the current x cordinate of the spaceship
                    pillX = doctorX
                    fire_pill(pillX, pillY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                doctorX_change = 0


    doctorX += doctorX_change
    if doctorX <= 0:
        doctorX = 0
    elif doctorX >= 736:
        doctorX = 736

    # victim Movement
    for i in range(num_of_victim):

        # Game Over
        if victimY[i] > 300:
            for j in range(num_of_victim):
                victimY[j] = 2000
            game_over_text()
            break

        victimX[i] += victimX_change[i]
        if victimX[i] <= 0:
            victimX_change[i] = 4
            victimY[i] += victimY_change[i]
        elif victimX[i] >= 736:
            victimX_change[i] = -4
            victimY[i] += victimY_change[i]

        # Collision
        collision = isCollision(victimX[i], victimY[i], pillX, pillY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            pillY = 480
            pill_state = "ready"
            score_value += 1
            victimX[i] = random.randint(0, 736)
            victimY[i] = random.randint(50, 150)

        victim(victimX[i], victimY[i], i)

    # pill Movement
    if pillY <= 0:
        pillY = 480
        pill_state = "ready"

    if pill_state == "fire":
        fire_pill(pillX, pillY)
        pillY -= pillY_change

    doctor(doctorX, doctorY)
    show_score(textX, testY)
    pygame.display.update()
