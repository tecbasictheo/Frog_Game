# constants and imports
import time
import pygame

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 850
BOTTOM_BOUNDARY = 5
WIN_BOUNDARY = 10
WATER_ZONE = pygame.Rect(20, 20, 700, 700)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg_image = pygame.image.load("media/background.png")
bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH + 50, SCREEN_HEIGHT + 25))


from frog import *
from enum import Enum
import math
import random

run = True
jumping = False
game_over = False
GAME_STATE = "MENU"
clock = pygame.time.Clock()
pygame.display.set_caption("Frog Game")
BACKGROUND_COLOR = "light blue"
Initial_X = SCREEN_WIDTH // 2
Initial_Y = 845
LANE_HEIGHT = 150
current_level = 1
Show_text = False
text_start_time = 0
text_duration = 2.0
frog_rotation_angle = 0

#sound setup
falling_water_sound = pygame.mixer.Sound("media/falling_water.wav")
water_sound = pygame.mixer.Sound("media/water_moving.wav")
background_music = pygame.mixer.Sound("media/music.wav")

water_sound_playing = False
background_music_playing = False

#level setup
levels = {
    1: {  # Level 1
        'lanes': [
            {'petals': 5, 'spacing': 150, 'speed': 2, 'direction': 1, 'y_pos': 622},
            {'petals': 4, 'spacing': 200, 'speed': 1.5, 'direction': -1, 'y_pos': 455},
            {'petals': 5, 'spacing': 170, 'speed': 2, 'direction': -1, 'y_pos': 285},
            {'petals': 3, 'spacing': 300, 'speed': 1, 'direction': 1, 'y_pos': 130},
            {'petals': 5, 'spacing': 200, 'speed': 1.75, 'direction': -1, 'y_pos': 8},
        ]
    },
    2: {
        'lanes': [
            {'petals': 6, 'spacing': 150, 'speed': 2, 'direction': -1, 'y_pos': 622},
            {'petals': 5, 'spacing': 160, 'speed': 3, 'direction': -1, 'y_pos': 455},
            {'petals': 4, 'spacing': 250, 'speed': 1.5, 'direction': 1, 'y_pos': 285},
            {'petals': 5, 'spacing': 180, 'speed': 1.25, 'direction': -1, 'y_pos': 130},
            {'petals': 4, 'spacing': 290, 'speed': 1, 'direction': -1, 'y_pos': 8},
        ]
    },
    3: {
        'lanes': [
            {'petals': 6, 'spacing': 150, 'speed': 2, 'direction': -1, 'y_pos': 622},
            {'petals': 5, 'spacing': 190, 'speed': 1, 'direction': -1, 'y_pos': 455},
            {'petals': 4, 'spacing': 200, 'speed': 1, 'direction': -1, 'y_pos': 285},
            {'petals': 3, 'spacing': 200, 'speed': 1.5, 'direction': 1, 'y_pos': 130},
            {'petals': 4, 'spacing': 290, 'speed': 1, 'direction': 1, 'y_pos': 5},
        ]
    }
}
LANE_COUNT = len(levels[current_level]['lanes'])

# frog direction setup
class Direction(Enum):
    UP = 0
    DOWN = 180
    LEFT = 270
    RIGHT = 90
# petals: setup, classes
Petal_Images = [
    "media/Petal1_y.png",
    "media/Petal2_y.png",
    "media/Petal3_y.png"
]

class Petal(pygame.sprite.Sprite):

    def __init__(self, lane):
        super().__init__()

        image_choice = random.choice(Petal_Images)
        self.image = pygame.image.load(image_choice).convert_alpha()
        self.image = pygame.transform.scale(self.image, (130, 130))
        self.rect = self.image.get_rect()
        self.speed = 1.5
        self.mask = pygame.mask.from_surface(self.image, 50)
        self.lane = lane
        self.screen_width = SCREEN_WIDTH
        self.direction = direction

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0 or self.rect.left > self.screen_width:
            self.reset_position()

    def reset_position(self):
        if self.direction > 0:
            self.rect.left = -self.rect.width
        else:
            self.rect.right = self.screen_width + self.rect.width

#startpoint class
class Start():
    def __init__(self):
        self.image = pygame.image.load("media/Petal2_y.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (125, 125))
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.x_st = 335
        self.y_st = 730
        self.rect.x = self.x_st
        self.rect.y = self.y_st

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.image, (600,730))
        screen.blit(self.image, (100,720))
        self.image_u = pygame.transform.rotate(self.image, 10)
        screen.blit(self.image_u, (211, 740)) #starter point ->  try out
        screen.blit(self.image_u, (-35, 720)) #starter point ->  try out
        self.image_o = pygame.transform.rotate(self.image, 190)
        screen.blit(self.image_o, (460, 732))
        screen.blit(self.image_o, (710, 735))


# all functions for the Game
def load_level(level_number):
    level_data = levels[level_number]
    return level_data['lanes']

def render_mainmenu():
    global frog_rotation_angle
    screen.blit(bg, (0, 0))
    frog_rotation_angle -= 2
    if frog_rotation_angle >= 360:
        frog_rotation_angle = 0
    Frog_si = pygame.transform.scale(Sitting_f, (w_1 * 0.6, h_1 * 0.6))
    Frog_si = pygame.transform.rotate(Frog_si, frog_rotation_angle)
    Frog_rect = Frog_si.get_rect(center=(400, 500))
    screen.blit(Frog_si, Frog_rect)
    font = pygame.font.SysFont('Herculanum', 90)
    title = font.render("FROGGER", True, (60, 179, 113))
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(title, title_rect)

    font = pygame.font.SysFont('Times New Roman', 25)
    start_text = font.render("Press space for start", True, (0,0,0))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
    screen.blit(start_text, start_rect)
    font = pygame.font.SysFont('Times New Roman', 25)
    start_text_p = font.render("< Change angle >", True, (0,0,0))
    start_rect_p = start_text_p.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200))
    screen.blit(start_text_p, start_rect_p)

def main_menu():
    global GAME_STATE
    render_mainmenu()
    pygame.display.update()
    pygame.display.flip()

def advance_level(screen):
    global current_level, petal_group, LANE_COUNT, jumping, frog_angle, GAME_STATE, game_over
    current_level += 1
    if current_level > len(levels):
        font = pygame.font.SysFont('Times New Roman', 38)
        text_surface = font.render("You win!", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        time.sleep(1)

        current_level = 1
        GAME_STATE = "MENU"
        game_over = False
        petal_group.empty()
        return False

    LANE_COUNT = len(levels[current_level]['lanes'])
    petal_group.empty()

    for lane in range(LANE_COUNT):
        lane_config = levels[current_level]['lanes'][lane]
        for i in range(lane_config['petals']):
            new_petal = Petal(lane)
            new_petal.rect.x = i * lane_config['spacing'] + 50
            new_petal.rect.y = lane_config['y_pos']
            new_petal.speed = lane_config['speed']
            new_petal.direction = lane_config['direction']
            petal_group.add(new_petal)

    if current_level != 1:
        font = pygame.font.SysFont('Times New Roman', 38)
        text_surface = font.render("Level up!", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        jumping = False
        frog_angle = Direction.UP.value
        pygame.display.update()
        time.sleep(1)
        return True

def show_game_over_screen():
    global GAME_STATE
    screen.blit(bg, (0, 0))
    font = pygame.font.SysFont('Herculanum', 72)
    text = font.render("You died", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    font = pygame.font.SysFont('Times New Roman', 25)
    restart_text = font.render("Press space for restart", True, (0, 0, 0))
    restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
    screen.blit(restart_text, restart_text_rect)
    menu_text = font.render("Press m for menu", True, (0, 0, 0))
    menu_text_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200))
    screen.blit(menu_text, menu_text_rect)

def restart_game():
    global X_POSITION, Y_POSITION, game_over, run, jumping, frog_angle, GAME_STATE, current_level, LANE_COUNT
    GAME_STATE = "RESTART"
    X_POSITION = Initial_X
    Y_POSITION = Initial_Y
    jumping = False
    frog_angle = Direction.UP.value
    game_over = False
    GAME_STATE = "PLAYING"

    LANE_COUNT = len(levels[current_level]['lanes'])

    frog.rect.center = (X_POSITION, Y_POSITION)
    frog.jumping = False
    frog.on_petal = False
    frog.current_petal = None
    current_level = 1

    LANE_COUNT = len(levels[current_level]['lanes'])
    petal_group.empty()

    for lane in range(LANE_COUNT):
        lane_config = levels[current_level]['lanes'][lane]
        for i in range(lane_config['petals']):
            new_petal = Petal(lane)
            new_petal.rect.x = i * lane_config['spacing'] + 50
            new_petal.rect.y = lane_config['y_pos']
            new_petal.speed = lane_config['speed']
            new_petal.direction = lane_config['direction']
            petal_group.add(new_petal)

def restart_level():
    global X_POSITION, Y_POSITION, game_over, run, jumping, frog_angle, GAME_STATE, current_level, LANE_COUNT
    GAME_STATE = "RESTART"
    X_POSITION = Initial_X
    Y_POSITION = Initial_Y
    jumping = False
    frog_angle = Direction.UP.value
    game_over = False
    GAME_STATE = "PLAYING"

    LANE_COUNT = len(levels[current_level]['lanes'])

    frog.rect.center = (X_POSITION, Y_POSITION)
    frog.jumping = False
    frog.on_petal = False
    frog.current_petal = None
    current_level = current_level

    LANE_COUNT = len(levels[current_level]['lanes'])
    petal_group.empty()

    for lane in range(LANE_COUNT):
        lane_config = levels[current_level]['lanes'][lane]
        for i in range(lane_config['petals']):
            new_petal = Petal(lane)
            new_petal.rect.x = i * lane_config['spacing'] + 50
            new_petal.rect.y = lane_config['y_pos']
            new_petal.speed = lane_config['speed']
            new_petal.direction = lane_config['direction']
            petal_group.add(new_petal)

def level_completion():
    global X_POSITION, Y_POSITION

    if Y_POSITION < 0:
        return True
    return False

def handle_collision(frog, petal_group):
        collided_petal = pygame.sprite.spritecollideany(frog, petal_group, pygame.sprite.collide_mask)

        if collided_petal and not frog.on_petal:
            frog.attach_to_petal(collided_petal)
            frog.on_petal = True
            frog.current_petal = collided_petal
            frog.jumping = False
            frog.update_image()

            global X_POSITION, Y_POSITION
            X_POSITION = frog.rect.centerx
            Y_POSITION = frog.rect.centery
            return True

        return False
# setup before game loop
lane_configs = load_level(current_level)
start = Start()
frog_group = pygame.sprite.Group()
frog = Frog(Initial_X, 730)
petal_group = pygame.sprite.Group()
frog_group.add(frog)

for lane in range(LANE_COUNT):
    lane_config = levels[current_level]['lanes'][lane]
    for i in range(lane_config['petals']):
        new_petal = Petal(lane)
        new_petal.rect.x = i * lane_config['spacing'] + 50
        new_petal.rect.y = lane_config['y_pos']
        new_petal.speed = lane_config['speed']
        new_petal.direction = lane_config['direction']
        petal_group.add(new_petal)

GAME_STATE = "MENU"
main_menu()
background_music.play(-1)
background_music_playing = True
# Game loop
while run:
    dt = clock.tick(60) / 1000.0
    if GAME_STATE == "MENU":
        water_sound.stop()
        water_sound_playing = False
        render_mainmenu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    GAME_STATE = "PLAYING"
                    X_POSITION = Initial_X
                    Y_POSITION = Initial_Y
                    LANE_COUNT = len(levels[current_level]['lanes'])
                    frog.rect.center = (X_POSITION, Y_POSITION)
                    jumping = False
                    frog.jumping = False
                    frog.on_petal = False
                    frog.current_petal = None
                    petal_group.empty()
                    for lane in range(LANE_COUNT):
                        lane_config = levels[current_level]['lanes'][lane]
                        for i in range(lane_config['petals']):
                            new_petal = Petal(lane)
                            new_petal.rect.x = i * lane_config['spacing'] + 50
                            new_petal.rect.y = lane_config['y_pos']
                            new_petal.speed = lane_config['speed']
                            new_petal.direction = lane_config['direction']
                            petal_group.add(new_petal)

    elif GAME_STATE == "RESTART":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart_game()
                    game_over = False
                    water_sound_playing = False

    elif GAME_STATE == "PLAYING":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not jumping:
                                if frog.on_petal:
                                    frog.on_petal = False
                                    frog.current_petal = None
                                    frog.rect.y -= 25 #pos above petal
                                    Y_POSITION = frog.rect.centery
                                jumping = True
                                frog.jumping = True
                                Y_VELOCITY = JUMP_HEIGHT
                                frog.update_image()

            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not jumping:
                            if frog.on_petal:
                                frog.detach_from_petal()

                            jumping = True
                            frog.jumping = True
                            Y_VELOCITY = JUMP_HEIGHT
                            frog.update_image()
                            frog.angle = 0


        if not game_over:
            if not water_sound_playing:
                water_sound.play(-1)
                water_sound_playing = True

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT]:
                frog_angle += 2
            if keys_pressed[pygame.K_RIGHT]:
                frog_angle -= 2

            if jumping:
                angle_rad = math.radians(270 - frog_angle)
                dx = math.cos(angle_rad) * JUMP_Speed
                dy = math.sin(angle_rad) * JUMP_Speed
                X_POSITION += dx
                Y_POSITION += dy
                Y_VELOCITY -= Y_GRAVITY

                frog.rect.center = (X_POSITION, Y_POSITION)
                frog.angle = frog_angle
                frog.update()

                if Y_VELOCITY < -JUMP_HEIGHT:
                    jumping = False
                    Y_VELOCITY = JUMP_HEIGHT
                    frog.jumping = False
                    frog.update_image()
                    frog.update()
            else:
                frog.rect.center = (X_POSITION, Y_POSITION)
                frog.angle = frog_angle
                frog.update()

            if not jumping and frog.on_petal and frog.current_petal:
                    frog.rect.x = frog.current_petal.rect.x
                    frog.rect.y = frog.current_petal.rect.y
                    X_POSITION = frog.rect.centerx
                    Y_POSITION = frog.rect.centery
                    frog.update()

            frog.update_image()
            screen.fill(BACKGROUND_COLOR)
            petal_group.update()
            petal_group.draw(screen)
            frog_group.update()
            start.draw(screen)
            frog.draw(screen)
            frog_group.update()
            frog.update()
            on_petal = pygame.sprite.spritecollideany(frog, petal_group, pygame.sprite.collide_mask)
            fall_water = frog.rect.colliderect(WATER_ZONE)

            BOTTOM_BOUNDARY = 50
            if Y_POSITION > SCREEN_HEIGHT - BOTTOM_BOUNDARY:
                Y_POSITION = (SCREEN_HEIGHT - BOTTOM_BOUNDARY)

            if SCREEN_WIDTH + 20 < X_POSITION or X_POSITION < 0 -20:
                game_over = True

            if on_petal:
                handle_collision(frog, petal_group)

            if frog.on_petal and frog.current_petal:
                frog.rect.centerx = frog.current_petal.rect.centerx + frog.offset_x
                frog.rect.bottom = frog.current_petal.rect.top + frog.offset_y

            if level_completion():
                frog.jumping = False
                if not advance_level(screen):
                    pass
                else:
                    X_POSITION = Initial_X
                    Y_POSITION = Initial_Y
                    frog.update()
                    game_over = False

            elif (not on_petal) and (not frog.jumping) and fall_water:
                falling_water_sound.play()
                game_over = True

        if game_over:
            water_sound.stop()
            water_sound_playing = False
            GAME_STATE = "GAME_OVER"

    elif GAME_STATE == "GAME_OVER":
        water_sound.stop()
        water_sound_playing = False
        show_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart_level()
                if event.key == pygame.K_m:
                    GAME_STATE = "MENU"
                    current_level = 1
                    LANE_COUNT = len(levels[current_level]['lanes'])
                    X_POSITION = Initial_X
                    Y_POSITION = Initial_Y
                    frog.rect.center = (X_POSITION, Y_POSITION)
                    jumping = False
                    frog.jumping = False
                    game_over = False


    pygame.display.flip()
    pygame.display.update()

pygame.quit()
exit()