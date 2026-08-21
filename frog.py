import pygame
import sys
import math

pygame.init()
exitgame = False
jumping = False
Y_GRAVITY = 1
JUMP_HEIGHT = 12 # abstand petals 10
Y_VELOCITY = JUMP_HEIGHT
frog_angle = 0
JUMP_Speed = 5

'''
Clock = pygame.time.Clock()
Screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Frog_jumping")

BACKGROUND_COLOR = ("light blue")
Background_f = BACKGROUND_COLOR '''
X_POSITION, Y_POSITION = 400, 750

Sitting_f = pygame.image.load("media/frog_sitting.png").convert_alpha()
w_1 = Sitting_f.get_width()
h_1 = Sitting_f.get_height()
Frog_s = pygame.transform.scale(Sitting_f, (w_1 * 0.25, h_1 * 0.25))
Jumping_f = pygame.image.load("media/frog_jumping.png").convert_alpha()
w_2 = Jumping_f.get_width()
h_2 = Jumping_f.get_height()
Frog_j = pygame.transform.scale(Jumping_f, (w_2 * 0.45, h_2 * 0.45))
frog_jump = Frog_s.get_rect(center=(X_POSITION, Y_POSITION))
rotated_frog = pygame.transform.rotate(Frog_j, frog_angle)
'''
while True:

    Clock.tick(60)
    Screen.fill(Background_f)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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

    if jumping:
        angle_rad = math.radians(270 - frog_angle) # convert angle to radians
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
'''