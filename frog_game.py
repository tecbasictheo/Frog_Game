import time

import pygame

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 850
BOTTOM_BOUNDARY = 5
WIN_BOUNDARY = 10
WATER_ZONE = pygame.Rect(20, 20, 700, 700)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

from frog import *
from enum import Enum
import math

#on_petal = pygame.sprite.spritecollideany(frog, petal_group, pygame.sprite.collide_mask)
run = True
jumping = False
game_over = False
GAME_STATE = "MENU"
restart_button = None
main_menu_button = None
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
            {'petals': 4, 'spacing': 250, 'speed': 3, 'direction': -1, 'y_pos': 475},
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

    def draw_mask_debug(self, screen):
        """Draw the mask outline for debugging"""
        if hasattr(self, 'mask') and self.mask:
            # Get the mask as a surface (white where mask exists, transparent elsewhere)
            mask_surface = self.mask.to_surface()
            # Draw it at the frog's position
            screen.blit(mask_surface, self.rect.topleft)


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
                            petal = Petal(lane)
                            self.petals.append(petal)
                            self.count += 1
                    if self.count == self.max_count // 2:
                        self.spawn_delay = 2
                        self.timer = 0

    def draw(self):
        for petal in self.petals:
            petal.draw()

    def spawn_petal(self, lane, lane_config):
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

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        #Screen.blit(self.mask, self.rect)


def load_level(level_number):
    level_data = levels[level_number]
    return level_data['lanes']


def render_mainmenu():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('Arial', 72, bold=True)
    title = font.render("FROGGER", True, (0, 255, 0))
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(title, title_rect)

    font = pygame.font.SysFont('Arial', 24)
    start_text = font.render("PRESS SPACE TO START", True, (255, 255, 0))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
    screen.blit(start_text, start_rect)

def main_menu():
    global GAME_STATE
    render_mainmenu()
    pygame.display.update()
    pygame.display.flip()

def advance_level(screen):
    global current_level, petal_group, LANE_COUNT, jumping, frog_angle, GAME_STATE, game_over
    current_level += 1
    if current_level > len(levels):
        font = pygame.font.SysFont('Times New Roman', 50)
        text_surface = font.render("You WIN!", True, (0, 0, 0))
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
        font = pygame.font.SysFont('Times New Roman', 30)
        text_surface = font.render("Level UP!", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        jumping = False
        frog_angle = Direction.UP.value
        pygame.display.update()
        time.sleep(1)
        return True

def show_game_over_screen():
    global GAME_STATE
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 72)  # Large font
    text = font.render("You died", True, (255, 0, 0))  # Red text
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    GAME_STATE = "RESTART"

    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 50)
    pygame.draw.rect(screen, (0, 255, 0), restart_button)  # Green button
    restart_text = font.render("Restart", True, (0, 0, 0))
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, restart_text_rect)
    main_menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100, 200, 100)
    pygame.draw.rect(screen, (0, 255, 0), main_menu_button)  # Green button
    menu_text = font.render("menu_text", True, (0, 0, 0))
    menu_text_rect = menu_text.get_rect(center=main_menu_button.center)
    screen.blit(menu_text, menu_text_rect)
    return restart_button, main_menu_button

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


def level_completion():
    global X_POSITION, Y_POSITION

    if Y_POSITION < 0:
        return True
    return False


def handle_collision(frog, petal_group):
        # Check for collision with any petal using mask collision
        collided_petal = pygame.sprite.spritecollideany(frog, petal_group, pygame.sprite.collide_mask)

        if collided_petal and not frog.on_petal:
            frog.attach_to_petal(collided_petal)
            frog.on_petal = True
            frog.current_petal = collided_petal
            frog.jumping = False
            frog.update_image()  # sitting image

            global X_POSITION, Y_POSITION
            X_POSITION = frog.rect.centerx
            Y_POSITION = frog.rect.centery

            print("Frog landed on petal!")
            return True

        return False

def jump_frog(frog, X_POSITION, Y_POSITION):
    if frog.on_petal:
        X_POSITION = frog.rect.centerx
        Y_POSITION = frog.rect.centery
        frog.on_petal = False
        frog.current_petal = None

def draw_mask(surface, sprite, color=(0, 255, 0)):
    mask_outline = sprite.mask.outline()
    if mask_outline:
        # Shift points to match sprite position
        points = [(x + sprite.rect.x, y + sprite.rect.y) for x, y in mask_outline]
        pygame.draw.polygon(surface, color, points, 2)  # Thicker line for visibility

lane_configs = load_level(current_level)
start = Start()
spawner = PetalSpawner(SCREEN_WIDTH)
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
_last_mask_real = None
GAME_STATE = "MENU"
main_menu()
while run:
    dt = clock.tick(60) / 1000.0
    if GAME_STATE == "MENU":
        render_mainmenu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    GAME_STATE = "PLAYING"
                    X_POSITION = Initial_X
                    Y_POSITION = Initial_Y
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

        #pygame.display.flip()
        #continue
    elif GAME_STATE == "PLAYING":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not jumping:
                                if frog.on_petal:
                                    # Jumping from a petal
                                    frog.on_petal = False
                                    frog.current_petal = None
                                    # Position frog slightly above the petal for the jump
                                    frog.rect.y -= 50
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

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT]:
                frog_angle += 2
            if keys_pressed[pygame.K_RIGHT]:
                frog_angle -= 2

            if jumping:
                angle_rad = math.radians(270 - frog_angle)  # convert angle to radians
                dx = math.cos(angle_rad) * JUMP_Speed
                dy = math.sin(angle_rad) * JUMP_Speed
                X_POSITION += dx
                Y_POSITION += dy
                Y_VELOCITY -= Y_GRAVITY

                frog.rect.center = (X_POSITION, Y_POSITION)
                frog.angle = frog_angle
                frog.update_hitbox()

                if Y_VELOCITY < -JUMP_HEIGHT:
                    jumping = False
                    Y_VELOCITY = JUMP_HEIGHT
                    frog.jumping = False
                    frog.update_image()
                    frog.update_hitbox()
            else:
                frog.rect.center = (X_POSITION, Y_POSITION)
                frog.angle = frog_angle
                frog.update_hitbox()

            if not jumping and frog.on_petal and frog.current_petal:
                    frog.rect.x = frog.current_petal.rect.x
                    frog.rect.y = frog.current_petal.rect.y
                    X_POSITION = frog.rect.centerx
                    Y_POSITION = frog.rect.centery
                    frog.update_hitbox()

            frog.update_image()
            screen.fill(BACKGROUND_COLOR)
            spawner.update(dt)

            petal_group.update()
            petal_group.draw(screen)
            frog_group.update()
            start.draw(screen)
            frog.draw(screen)
            frog_group.update()
            frog.update_hitbox()
            on_petal = pygame.sprite.spritecollideany(frog, petal_group, pygame.sprite.collide_mask)
            fall_water = frog.rect.colliderect(WATER_ZONE)

            if hasattr(frog, "mask") and frog.mask is not None:
                mask_real = (frog.mask.count() > 0)
            else:
                mask_real = False

            if mask_real != _last_mask_real:
                print(
                    f"[mask debug] frog.mask.count() = {frog.mask.count() if hasattr(frog, 'mask') and frog.mask is not None else 'None'} -> real = {mask_real}")
                _last_mask_real = mask_real

            for petal in spawner.petals:
                screen.blit(petal.image, petal.rect)
            for petal in petal_group:
                petal.mask = pygame.mask.from_surface(petal.image)
            #pygame.draw.rect(screen, (0, 100, 255), WATER_ZONE)

            BOTTOM_BOUNDARY = 50
            if Y_POSITION > (SCREEN_HEIGHT) - BOTTOM_BOUNDARY:
                Y_POSITION = ((SCREEN_HEIGHT) - BOTTOM_BOUNDARY)

            if SCREEN_WIDTH + 20 < X_POSITION or X_POSITION < 0 -20:
                game_over = True

            if on_petal:
                print("collision")
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
                    frog.update_hitbox()
                    game_over = False

            elif (not on_petal) and (not frog.jumping) and fall_water:
                print("Frog in water and not on petal -> game over")
                print(Y_POSITION)
                print(f"frog.rect={frog.rect}, WATER_ZONE={WATER_ZONE}, fall_water={fall_water}, on_petal={bool(on_petal)}, jumping={frog.jumping}")
                print("frog.rect=", frog.rect, "hitbox=", frog.hitbox_rect)
                game_over = True

        if game_over:
            GAME_STATE = "GAME_OVER"

    elif GAME_STATE == "GAME_OVER":
        show_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE:
                    restart_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l: #does not work
                    main_menu()
                    current_level = 1
                    X_POSITION = Initial_X
                    Y_POSITION = Initial_Y
                    frog.rect.center = (X_POSITION, Y_POSITION)
                    jumping = False
                    frog.jumping = False

    for petal in petal_group:
        draw_mask(screen, petal, (255, 0, 0))


    pygame.display.flip()
    pygame.display.update()

pygame.quit()
exit()