# from frog_game import Initial_Y, Initial_X
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
        self.rect = self.image.get_rect(center=(x, y))
        self.dir = direction
        self.angle = frog_angle
        self.screen = None
        self.x_pos = float(x)
        self.y_pos = float(y)
        self.hitbox_size = (30, 30)
        self.hitbox_surface = pygame.Surface(self.hitbox_size, pygame.SRCALPHA)
        pygame.draw.ellipse(self.hitbox_surface, (255, 255, 255), (0, 0, 30, 30))
        self.hitbox_offset = (0, 0)
        self.speed = 5
        self.offset_x = 0  # Initialize these here
        self.offset_y = 0  # Initialize these here

        # Store position
        self.x_pos = float(x)
        self.y_pos = float(y)

        # Initialize rect to match position
        self.rect = self.sitting_image.get_rect(center=(x, y))

        # Make sure rect matches position immediately
        self.rect.centerx = self.x_pos
        self.rect.centery = self.y_pos

        # Create hitbox for SITTING frog
        self.sitting_hitbox_size = (self.sitting_image.get_width() * 0.6,
                                    self.sitting_image.get_height() * 0.6)
        self.sitting_hitbox_surface = pygame.Surface(self.sitting_hitbox_size, pygame.SRCALPHA)
        pygame.draw.ellipse(self.sitting_hitbox_surface, (255, 255, 255),
                            (0, 0, *self.sitting_hitbox_size))

        # Start with sitting hitbox
        self.current_hitbox_surface = self.sitting_hitbox_surface
        self.mask = pygame.mask.from_surface(self.current_hitbox_surface)

        # Calculate offsets - these should center the hitbox on the frog
        self.sitting_hitbox_offset = (
            (self.sitting_image.get_width() - self.sitting_hitbox_size[0]) / 2,
            (self.sitting_image.get_height() - self.sitting_hitbox_size[1]) / 2
        )


    def update_image(self):
        if self.jumping:
            self.image = self.jumping_image
        else:
            self.image = self.sitting_image
            self.current_hitbox_surface = self.sitting_hitbox_surface
            self.hitbox_offset = self.sitting_hitbox_offset

            # Update mask to match current hitbox
            self.mask = pygame.mask.from_surface(self.current_hitbox_surface)

        # Update rect to match new image, but keep position
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)


    def draw_masks(self):
        pygame.draw.rect(self.screen, (0, 255, 0), self.frog.rect, 2)


    def draw(self, Screen):
        Screen.blit(self.image, self.rect)


    def get_hitbox_rect(self):
        """Get the hitbox rect positioned correctly relative to the frog"""
        """Get the hitbox rect positioned correctly relative to the frog"""
        hitbox_rect = self.current_hitbox_surface.get_rect(center=self.rect.center)
        hitbox_rect.x += self.hitbox_offset[0]
        hitbox_rect.y += self.hitbox_offset[1]
        return hitbox_rect


    def draw_hitbox(self, screen):
        """Draw the hitbox to see where it actually is"""
        hitbox_rect = self.get_hitbox_rect()
        pygame.draw.rect(screen, (255, 0, 0), hitbox_rect, 2)  # Red rectangle
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)  # Green frog rect
