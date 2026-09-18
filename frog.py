import pygame.draw

pygame.init()

jumping = False
JUMP_HEIGHT = 4
JUMP_Speed = 7
Y_VELOCITY = JUMP_HEIGHT
Y_GRAVITY = 1
frog_angle = 0
direction = frog_angle
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 850
LANE_HEIGHT = 170
X_POSITION, Y_POSITION = 400, 825
Initial_X = SCREEN_WIDTH // 2
Initial_Y = 825

# Frog image formats
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

#Frog class with petal-attach and -detach methods and creation of frog.hitbox
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

        self.mask = pygame.mask.from_surface(self.sitting_image)
        self.hitbox_rect = self.rect.inflate(-int(self.rect.width * 1), -int(self.rect.height * 1))

    def attach_to_petal(self, petal):
        self.current_petal = petal
        self.on_petal = True
        self.jumping = False
        old_center = self.rect.center
        self.update_image()
        self.rect = self.image.get_rect(center=old_center)

    def detach_from_petal(self):
         old_center = self.rect.center
         self.current_petal = None
         self.on_petal = False
         self.jumping = True
         self.update_image()
         self.rect = self.image.get_rect(center=old_center)

    def update_image(self):
            old_center = getattr(self, "rect", pygame.Rect(0, 0, 0, 0)).center
            self.image = self.jumping_image if self.jumping else self.sitting_image
            self.rect = self.image.get_rect(center=old_center)
            if not self.jumping:
                w, h = self.sitting_image.get_size()
                scale = 0.6
                small = pygame.transform.smoothscale(self.sitting_image, (int(w * scale), int(h * scale)))
                small_surf = pygame.Surface((w, h), pygame.SRCALPHA)
                pos = ((w - small.get_width()) // 2, (h - small.get_height()) // 2)
                small_surf.blit(small, pos)
                self.mask = pygame.mask.from_surface(small_surf)
            else:
                self.mask = pygame.mask.Mask((1, 1), False)

    def update(self):
        self.hitbox_rect = self.rect.inflate(-int(self.rect.width * 0.75), -int(self.rect.height * 0.75))

    def draw(self, Screen): #Screen works here as placeholder, will be overwritten in main file
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        Screen.blit(rotated_image, rotated_rect)

    def is_attached(self):
        return self.current_petal is not None

