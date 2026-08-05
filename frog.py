import pygame
import sys

pygame.init()

Clock = pygame.time.Clock()
Screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Frog_jumping")


X_POSITION, Y_POSITION = 400, 660

jumping = False

Y_GRAVITY = 1
JUMP_HEIGHT = 20
Y_VELOCITY = JUMP_HEIGHT

Sitting_f = pygame.image.load("media/frog_sitting.png").convert_alpha()
Frog_s = pygame.transform.scale(Sitting_f, (230,200))
Jumping_f = pygame.image.load("media/frog_jumping.png").convert_alpha()
Frog_j = pygame.transform.scale(Jumping_f, (300,360))

Background_f = ("blue")

frog_jump = Frog_s.get_rect(center=(X_POSITION, Y_POSITION))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_SPACE]:
        jumping = True

    BACKGROUND_COLOR = ("light blue")
    Background_f = BACKGROUND_COLOR
    #Screen.blit(Background_f, (0, 0))
    Screen.fill(BACKGROUND_COLOR)


    if jumping:
        Y_POSITION -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT
        frog_jump = Frog_s.get_rect(center=(X_POSITION - 45, Y_POSITION))
        Screen.blit(Frog_j, frog_jump)
    else:
        frog_jump = Frog_s.get_rect(center=(X_POSITION, Y_POSITION))
        Screen.blit(Frog_s, frog_jump)

    pygame.display.update()
    Clock.tick(60)

class Frog(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_frames()

    def load_frames(self):
        pygame.image.load("frog_sitting.png").convert_alpha()
        pygame.image.load("frog_jumping.png").convert_alpha()