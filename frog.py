# from frog_game import Initial_Y, Initial_X
import pygame.draw

from helper import *

pygame.init()
exitgame = False
jumping = False
Y_GRAVITY = 1
JUMP_HEIGHT = 20# abstand petals 10
Y_VELOCITY = JUMP_HEIGHT
frog_angle = 0
JUMP_Speed = 6
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
        self.offset_x = 0
        self.offset_y = 0
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.center = (x, y)
        self.attach = 0
        # Use the sprite image mask for collisions so mask + rect stay aligned
        # physics velocities (optional; keep if you use velocity-based jumps)
        self.vx = 0.0
        self.vy = 0.0

        # Use the sprite image as the mask so collide_mask uses the visible sprite area
        self.mask = pygame.mask.from_surface(self.sitting_image)
        # small debug hitbox rect (keeps aligned with sprite)
        self.hitbox_rect = self.rect.inflate(-int(self.rect.width * 1), -int(self.rect.height * 1))

    def attach_to_petal(self, petal):
        """Attach frog to a petal and sit the frog on top of it."""
        self.current_petal = petal
        self.on_petal = True
        self.jumping = False
        old_center = self.rect.center
        self.update_image()
     # Anchor the frog visually: bottom of frog sits at the top of the petal
        #self.rect.centerx = petal.rect.centerx
        #self.rect.bottom = petal.rect.top
        self.rect = self.image.get_rect(center=old_center)
        self.vx = 0.0
        self.vy = 0.0
    # keep mask aligned with current image

    def detach_from_petal(self):
         """Detach frog from current petal; preserve anchor so image swap doesn't pop visually."""
         old_center = self.rect.center
         self.current_petal = None
         self.on_petal = False
         self.jumping = True
         self.update_image()
         # preserve visual anchor when swapping images
         self.rect = self.image.get_rect(center=old_center)
         #self.mask = pygame.mask.from_surface(self.image)

    def update_image(self):
            old_center = getattr(self, "rect", pygame.Rect(0, 0, 0, 0)).center
            self.image = self.jumping_image if self.jumping else self.sitting_image
            self.rect = self.image.get_rect(center=old_center)
            # mask from sitting image if you want collisions only when sitting:
            if not self.jumping:
                #self.mask = pygame.mask.from_surface(self.sitting_image)
                w, h = self.sitting_image.get_size() # maybe this was size adjust
                scale = 0.6  # 60% size; change to 0.5 for smaller, 0.8 for larger
                small = pygame.transform.smoothscale(self.sitting_image, (int(w * scale), int(h * scale)))
                small_surf = pygame.Surface((w, h), pygame.SRCALPHA)
                pos = ((w - small.get_width()) // 2, (h - small.get_height()) // 2)
                small_surf.blit(small, pos)
                self.mask = pygame.mask.from_surface(small_surf)
            else:
                self.mask = pygame.mask.Mask((1, 1), False)

    def update(self):
            self.update_hitbox()
            #if self.current_petal is not None:
                #self.rect.centerx = self.current_petal.rect.centerx
                #self.rect.bottom = self.current_petal.rect.top + 2

    def update_hitbox(self):
        # keep mask aligned with visible image and update a smaller debug hitbox rect
        #self.mask = pygame.mask.from_surface(self.image)
        self.hitbox_rect = self.rect.inflate(-int(self.rect.width * 0.75), -int(self.rect.height * 0.75)) # maybe this is size adjust

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox_rect, 2)

    def draw(self, Screen):
        # Rotate the frog image based on the angle
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        # Get the rect of the rotated image and center it at the frog's position
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        # Draw the rotated frog image
        Screen.blit(rotated_image, rotated_rect)
        # Draw the hitbox
        self.draw_hitbox(Screen)

        # Debug: Draw attachment line if attached
        if self.current_petal is not None:
            pygame.draw.line(Screen, (0, 255, 0),
                             self.rect.center,
                             self.current_petal.rect.center, 2)

    def is_attached(self):
        return self.current_petal is not None

