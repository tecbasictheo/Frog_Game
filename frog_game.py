import pygame

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 850
BOTTOM_BOUNDARY = 50
WIN_BOUNDARY = 10
Screen = pygame.display.set_mode((800, 850))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

from helper import *
from frog import *
from enum import Enum

run = True
jumping = False
outside_screen = False # was maybe diffrernt scrreens for diffrent dying but does not worrk
game_over = False
fall_water = False
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

levels = {
    1: {  # Level 1
        'lanes': [
            {'petals': 3, 'spacing': 150, 'speed': 2, 'direction': 1, 'y_pos': 605},
            {'petals': 5, 'spacing': 300, 'speed': 3, 'direction': -1, 'y_pos': 475},
            {'petals': 4, 'spacing': 220, 'speed': 1.5, 'direction': 1, 'y_pos': 345},
            {'petals': 6, 'spacing': 150, 'speed': 3, 'direction': 1, 'y_pos': 215},
            {'petals': 5, 'spacing': 200, 'speed': 1.75, 'direction': -1, 'y_pos': 95},
        ]
        },
    2: {
        'lanes': [
            {'petals': 6, 'spacing': 150, 'speed': 2, 'direction': -1, 'y_pos': 605},
            {'petals': 5, 'spacing': 160, 'speed': 3, 'direction': -1, 'y_pos': 475},
            {'petals': 4, 'spacing': 170, 'speed': 5, 'direction': -1, 'y_pos': 345},
            {'petals': 5, 'spacing': 180, 'speed': 3, 'direction': -1, 'y_pos': 215},
            {'petals': 4, 'spacing': 290, 'speed': 1, 'direction': -1, 'y_pos': 95},
        ]
        },
    3: {
        'lanes': [
            {'petals': 6, 'spacing': 150, 'speed': 2, 'direction': -1, 'y_pos': 605},
            {'petals': 5, 'spacing': 160, 'speed': 3, 'direction': -1, 'y_pos': 475},
            {'petals': 4, 'spacing': 170, 'speed': 5, 'direction': -1, 'y_pos': 345},
            {'petals': 5, 'spacing': 180, 'speed': 3, 'direction': -1, 'y_pos': 215},
            {'petals': 4, 'spacing': 290, 'speed': 1, 'direction': -1, 'y_pos': 95},
        ]
        }
}

LANE_COUNT = len(levels[current_level]['lanes'])
Petal_Images = [
    "media/Petal1_y.png",
    "media/Petal2_y.png",
    "media/Petal3_y.png"
]

class Direction(Enum):
    UP = 0
    DOWN = 180
    LEFT = 270
    RIGHT = 90

class Petal(pygame.sprite.Sprite):

    def __init__(self, lane):
        super().__init__()

        image_choice = random.choice(Petal_Images)
        self.image = pygame.image.load(image_choice).convert_alpha()
        self.image = pygame.transform.scale(self.image, (125, 125))

        self.rect = self.image.get_rect()
        self.speed = 1.5
        self.mask = pygame.mask.from_surface(self.image)
        self.lane = lane
        self.screen_width = SCREEN_WIDTH

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0 or self.rect.left > self.screen_width:
            self.reset_position()

    def reset_position(self):
        if self.direction > 0:  # Moving right
            self.rect.left = -self.rect.width
        else:  # Moving left
            self.rect.right = self.screen_width + self.rect.width

class PetalSpawner:
    def __init__(self, screen_width):
        self.petals = []
        self.screen_width = screen_width
        self.max_count = 10
        self.count = 0
        self.spawn_delay = 1
        self.timer = 0

    def update(self, delta_time):
        for petal in self.petals[:]:
            petal.update(delta_time)

            if self.count < self.max_count:
                self.timer += delta_time
                if (petal.rect.right < 0 or petal.rect.left > self.screen_width):
                    self.petals.remove(petal)
                    self.spawn_petal(petal.lane)

                if self.timer > self.spawn_delay:
                    for lane in range(LANE_COUNT):
                        current_count = len([p for p in self.petals if p.lane == lane])
                        if current_count < self.petals_per_lane[lane]:
                            petal = Petal (lane)
                            self.petals.append(petal)
                            self.count += 1
                    if self.count == self.max_count // 2:
                        self.spawn_delay = 2
                        self.timer = 0

    def draw(self):
        for petal in self.petals:
            petal.draw()

    def spawn_petal(self, lane):
        lane_config = self.get_lane_config(lane)
        petal = Petal(lane, self.screen_width)
        self.petals.append(petal)
        self.spawn_delay

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

    def draw(self, Screen):
        Screen.blit(self.image, self.rect)

def load_level(level_number):
    level_data = levels[level_number]
    return level_data['lanes']

lane_configs = load_level(current_level)

def advance_level(Screen):
    global current_level, petal_group, LANE_COUNT, jumping, frog_angle
    current_level += 1
    if current_level > len(levels):
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

    if current_level != 1:
        font = pygame.font.SysFont('Times New Roman', 30)
        text_surface = font.render("Level UP!", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        jumping = False
        frog_angle = Direction.UP.value
        pygame.display.update()
        time.sleep(1)
        return True
    else: font = pygame.font.SysFont('Times New Roman', 50)
    text_surface = font.render("You WIN!", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    time.sleep(1) # move to main screen

def show_game_over_screen():
    Screen.fill((255,255,255))
    font = pygame.font.Font(None, 72)  # Large font
    text = font.render("You died", True, (255, 0, 0))  # Red text
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    Screen.blit(text, text_rect)

    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 50)
    pygame.draw.rect(screen, (0, 255, 0), restart_button)  # Green button
    restart_text = font.render("Restart", True, (0, 0, 0))
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    Screen.blit(restart_text, restart_text_rect)
    return restart_button

def restart_game():
    global X_POSITION, Y_POSITION, game_over, run, jumping, frog_angle
    X_POSITION = Initial_X
    Y_POSITION = Initial_Y
    jumping = False
    frog_angle = Direction.UP.value
    game_over = False

def level_completion():
    global X_POSITION, Y_POSITION
    if Y_POSITION < 0:
        return True
    return False

start = Start()
spawner = PetalSpawner(SCREEN_WIDTH)
frog_group = pygame.sprite.Group()
frog = Frog(Initial_X, Initial_Y)
petal_group = pygame.sprite.Group()
for lane in range(LANE_COUNT):
    lane_config = levels[current_level]['lanes'][lane]
    for i in range(lane_config['petals']):
        new_petal = Petal(lane)
        new_petal.rect.x = i * lane_config['spacing'] + 50
        new_petal.rect.y = lane_config['y_pos']
        new_petal.speed = lane_config['speed']
        new_petal.direction = lane_config['direction']
        petal_group.add(new_petal)

while run:
    clock.tick(60)
    dt = clock.tick(60) / 1000.0
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not jumping:
                    jumping = True
                    Y_VELOCITY = JUMP_HEIGHT
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                restart_game()
                game_over = False
    if not game_over:
        Screen.fill(BACKGROUND_COLOR)
        spawner.update(dt)
        # call menu
        # -> which calls the other game

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            frog_angle += 2
        if keys_pressed[pygame.K_RIGHT]:
            frog_angle -= 2

        if SCREEN_WIDTH < X_POSITION or X_POSITION < 0:
            game_over = True

        petal_group.update()
        petal_group.draw(Screen)
        frog_group.update()
        frog_group.draw(Screen)
        start.draw(Screen)
        for petal in spawner.petals:
            screen.blit(petal.image, petal.rect)

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

        BOTTOM_BOUNDARY = 50
        if Y_POSITION > (SCREEN_HEIGHT)  - BOTTOM_BOUNDARY:
            Y_POSITION = ((SCREEN_HEIGHT) - BOTTOM_BOUNDARY)

        if level_completion():
            advance_level(Screen)
            X_POSITION = Initial_X
            Y_POSITION = Initial_Y

        '''
               #mask collision
               frog_group.update()
               if pygame.sprite.spritecollide(frog_group, petal_group, False):
                   if pygame.sprite.spritecollide(frog_group, petal_group, False, pygame.sprite.collide_mask):
                      if Frog_s petal_group_mask.rect
               #stay in the petal : boundaries'''
        # fall water defineren

        #for level_one():

        # if outside of map end game
    elif game_over == True:
            restart_button = show_game_over_screen()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        restart_game()
                        game_over = False

    '''if water end game
    elif fall_water == True:  # if Frog_s not in ... :  #petal boundary
        if game_over == True:
        #run = False  # maybe das is falsch aber denke um den game loop neu zustarten
            restart_button = show_game_over_screen()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        restart_game()
                        game_over = False
    '''
    pygame.display.flip()
    pygame.display.update()



pygame.quit()
exit()
