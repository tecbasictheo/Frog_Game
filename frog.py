# from frog_game import Initial_Y, Initial_X
import pygame.draw

from helper import *

pygame.init()
exitgame = False
jumping = False
Y_GRAVITY = 1
JUMP_HEIGHT = 12  # abstand petals 10
Y_VELOCITY = JUMP_HEIGHT
frog_angle = 0
JUMP_Speed = 5.5
direction = frog_angle

X_POSITION, Y_POSITION = 400, 825
Initial_X = SCREEN_WIDTH // 2
Initial_Y = 825

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


class Frog(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.sitting_image = Frog_s
        self.jumping_image = Frog_j
        self.image = self.sitting_image
        self.on_petal = False
        self.current_petal = None
        self.jumping = False
        self.screen = None
        self.direction = direction
        self.speed = 5
        self.angle = frog_angle
        self.rect = self.image.get_rect(center=(x, y))
        self.x_pos = float(x)
        self.y_pos = float(y)
        self.rect.center = (x, y)
        self.hitbox_size = (self.sitting_image.get_width() * 0.3,
                    self.sitting_image.get_height() * 0.3)
        self.hitbox_surface = pygame.Surface(self.hitbox_size, pygame.SRCALPHA)
        pygame.draw.rect(self.hitbox_surface, (255, 255, 255),(0, 0, *self.hitbox_size))
        self.mask = pygame.mask.from_surface(self.hitbox_surface)
        self.hitbox_offset = (( (self.sitting_image.get_width() - self.hitbox_size[0]) / 2 - 50, (self.sitting_image.get_height() - self.hitbox_size[1]) / 2 - 30))

    def update_image(self):
        if self.jumping:
            self.image = self.jumping_image
        else:
            self.image = self.sitting_image

    def update_hitbox(self):
        # Get the current hitbox rect centered on the frog
        self.hitbox_rect = self.hitbox_surface.get_rect(center=self.rect.center)

        # Apply offset to position the hitbox correctly
        self.hitbox_rect.x += self.hitbox_offset[0]
        self.hitbox_rect.y += self.hitbox_offset[1]

        # If the frog is rotated, rotate the hitbox surface too
        if self.angle != 0:
            self.hitbox_surface_rotated = pygame.transform.rotate(
                self.hitbox_surface, self.angle)
            self.mask = pygame.mask.from_surface(self.hitbox_surface_rotated)
            # Recenter after rotation
            self.hitbox_rect = self.hitbox_surface_rotated.get_rect(center=self.rect.center)
        else:
            self.hitbox_surface_rotated = self.hitbox_surface

    def draw(self, Screen): # this works
        Screen.blit(self.image, self.rect)



