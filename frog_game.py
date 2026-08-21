import pygame
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
Screen = pygame.display.set_mode((800, 800))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

from helper import *
from frog import *
print("Helper imported!")

from random import randint


run = True
jumping = False
clock = pygame.time.Clock()
pygame.display.set_caption("Frog Game")
BACKGROUND_COLOR = ("light blue")

petal_group = pygame.sprite.Group()
for i in range(2):
    new_petal = Petal1()
    petal_group.add(new_petal)

#main game loop -> how to get everything in here
while run:
    clock.tick(60)

# call menu
# -> which calls the other game
    #quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not jumping:
                        jumping = True
                        Y_VELOCITY = JUMP_HEIGHT
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT]:
        frog_angle += 2
    if keys_pressed[pygame.K_RIGHT]:
        frog_angle -= 2

    petal_group.update()
    petal_group.draw(Screen)

    Screen.fill(BACKGROUND_COLOR)

    if jumping:
        angle_rad = math.radians(270 - frog_angle)  # convert angle to radians
        dx = math.cos(angle_rad) * JUMP_Speed
        dy = math.sin(angle_rad) * JUMP_Speed
        X_POSITION += dx
        Y_POSITION += dy
        Y_VELOCITY -= Y_GRAVITY
        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT
        frog_jump = Frog_j.get_rect(center=(X_POSITION, Y_POSITION))
        rotated_frog = pygame.transform.rotate(Frog_j, frog_angle)
        Screen.blit(rotated_frog, frog_jump)
    else:
        frog_jump = Frog_s.get_rect(center=(X_POSITION, Y_POSITION))
        rotated_frog = pygame.transform.rotate(Frog_s, frog_angle)
        frog_rect = rotated_frog.get_rect(center=(X_POSITION, Y_POSITION))
        Screen.blit(rotated_frog, frog_rect)


    pygame.display.flip()
    pygame.display.update()

pygame.quit()
exit()
