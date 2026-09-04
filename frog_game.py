import pygame

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 850
BOTTOM_BOUNDARY = 5
WIN_BOUNDARY = 10
Screen = pygame.display.set_mode((800, 850))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

from frog import *
from enum import Enum
import math

run = True
jumping = False
game_over = False
fall_water = False
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
            {'petals': 5, 'spacing': 250, 'speed': 3, 'direction': -1, 'y_pos': 475},
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
        self.rect = self.image.get_rect(center=(X_POSITION, Y_POSITION))
        self.speed = 1.5
        self.mask = pygame.mask.from_surface(self.image)
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
    else:
        font = pygame.font.SysFont('Times New Roman', 50)
    text_surface = font.render("You WIN!", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    time.sleep(1)  # move to main screen


def show_game_over_screen():
    Screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 72)  # Large font
    text = font.render("You died", True, (255, 0, 0))  # Red text
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    Screen.blit(text, text_rect)

    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 50)
    pygame.draw.rect(screen, (0, 255, 0), restart_button)  # Green button
    restart_text = font.render("Restart", True, (0, 0, 0))
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    Screen.blit(restart_text, restart_text_rect)
    main_menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100, 200, 100)
    pygame.draw.rect(screen, (0, 255, 0), main_menu_button)  # Green button
    menu_text = font.render("menu_text", True, (0, 0, 0))
    menu_text_rect = menu_text.get_rect(center=main_menu_button.center)
    Screen.blit(menu_text, menu_text_rect)
    return restart_button, main_menu_button

def main_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('Arial', 72, bold=True)
    title = font.render("FROGGER", True, (0, 255, 0))
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(title, title_rect)

    font = pygame.font.SysFont('Arial', 24)
    start_text = font.render("PRESS SPACE TO START", True, (255, 255, 0))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
    screen.blit(start_text, start_rect)

def restart_game():
    global X_POSITION, Y_POSITION, game_over, run, jumping, frog_angle, GAME_STATE, current_level
    X_POSITION = Initial_X
    Y_POSITION = Initial_Y
    jumping = False
    frog_angle = Direction.UP.value
    game_over = False
    GAME_STATE = "PLAYING"

    frog.rect.center = (X_POSITION, Y_POSITION)
    frog.jumping = False
    frog.on_petal = False
    frog.current_petal = None
    current_level = 1
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


def handle_landing(frog, petal_group):
    if frog.on_petal and frog.current_petal:
        if not frog.rect.colliderect(frog.current_petal.rect):
            frog.on_petal = False
            frog.current_petal = None
        else:
            move_x = frog.current_petal.speed * frog.current_petal.direction
            frog.rect.x += move_x
            frog.x_pos = frog.rect.centerx
            frog.y_pos = frog.rect.centery
    else:
        for petal in petal_group:
            if frog.rect.colliderect(petal.rect):  # Use rect collision
                frog.on_petal = True
                frog.current_petal = petal
                frog.rect.bottom = petal.rect.top
                frog.rect.centerx = petal.rect.centerx
                frog.x_pos = frog.rect.centerx
                frog.y_pos = frog.rect.centery
                print("Frog landed on petal!")
                break

        '''print(f"Frog on petal: {frog.on_petal}, current_petal: {frog.current_petal}")

        if frog.on_petal and frog.current_petal:
            print(f"Checking if still on petal: {frog.current_petal}")
            # Check if still on the same petal
            if not pygame.sprite.collide_mask(frog, frog.current_petal):
                print("Frog fell off petal!")
                frog.on_petal = False
                frog.current_petal = None
            else:
                print("Frog still on petal - moving with it!")
                # Move with the petal
                move_x = frog.current_petal.speed * frog.current_petal.direction
                print(f"Moving frog by {move_x} pixels")
                frog.rect.x += move_x
                # Update position variables to match
                frog.x_pos = frog.rect.centerx
                frog.y_pos = frog.rect.centery
        else:
            print("Checking for new petal collisions...")
            # Check for collision with any petal
            for petal in petal_group:
                collision = pygame.sprite.collide_mask(frog, petal)
                print(f"Checking collision with petal: {collision}")
                if collision:
                    print("Frog landed on a new petal!")
                    frog.on_petal = True
                    frog.current_petal = petal
                    # Position frog on top of petal
                    frog.rect.bottom = petal.rect.top
                    frog.rect.centerx = petal.rect.centerx
                    # Update position variables
                    frog.x_pos = frog.rect.centerx
                    frog.y_pos = frog.rect.centery
                    break'''

def draw_mask(surface, sprite, color=(0, 255, 0)):
    mask_outline = sprite.mask.outline()

    if mask_outline:
        points = [(x + sprite.rect.x, y + sprite.rect.y) for x, y in mask_outline]
        pygame.draw.polygon(surface, color, points, 1)


start = Start()
spawner = PetalSpawner(SCREEN_WIDTH)
frog_group = pygame.sprite.Group()
frog = Frog(Initial_X, 730)
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


def draw_rotated_mask_at_position(surface, x, y, angle, image, color=(0, 255, 0)):
    rotated_img = pygame.transform.rotate(image, angle)
    rotated_mask = pygame.mask.from_surface(rotated_img)
    outline = rotated_mask.outline()

    if outline:
        rect = rotated_img.get_rect(center=(x, y))
        points = [(x + rect.x, y + rect.y) for x, y in outline]
        pygame.draw.polygon(surface, color, points, 1)


while run:
    dt = clock.tick(60) / 1000.0
    if GAME_STATE == "MENU":
        main_menu()
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

        pygame.display.flip()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("SPACE PRESSED!")
                print(f"Before: frog.jumping={frog.jumping}, jumping={jumping}")
                if not jumping:
                    jumping = True
                    frog.jumping = True
                    print(f"After: frog.jumping={frog.jumping}")
                    Y_VELOCITY = JUMP_HEIGHT
                    if Y_VELOCITY < -JUMP_HEIGHT:
                        jumping = False
                        frog.jumping = False  # ← ADD THIS
                        Y_VELOCITY = JUMP_HEIGHT
                        frog.update_image()  # ← ADD THIS

        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                restart_game()
                game_over = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and frog.on_petal:
                frog.on_petal = False
                frog.current_petal = None
                frog.jumping = True

    if not game_over:
        frog.update_image()
        Screen.fill(BACKGROUND_COLOR)
        #screen.blit(frog.image, frog.rect)
        spawner.update(dt)
        #outline = frog.mask.outline()
        #if outline:
            #points = [(x + frog.rect.x, y + frog.rect.y) for x, y in outline]
            #pygame.draw.polygon(screen, (0, 255, 0), points, 1)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            frog_angle += 2
        if keys_pressed[pygame.K_RIGHT]:
            frog_angle -= 2

        if SCREEN_WIDTH < X_POSITION or X_POSITION < 0:
            game_over = True

        petal_group.update()
        petal_group.draw(Screen)
        start.draw(Screen)
        print(f"Frog jumping: {frog.jumping}")
        print(f"Frog image size: {frog.image.get_size()}")
        print(f"Frog mask size: {frog.mask.get_size()}")
        print(f"Frog mask outline points: {len(frog.mask.outline())}")
        frog.draw_hitbox(screen)

        for petal in spawner.petals:
            screen.blit(petal.image, petal.rect)


        if jumping:
            visual_offset_x = 0
            visual_offset_y = 0

            frog.rect.centerx = X_POSITION + visual_offset_x
            frog.rect.centery = Y_POSITION + visual_offset_y
            angle_rad = math.radians(270 - frog_angle)  # convert angle to radians
            dx = math.cos(angle_rad) * JUMP_Speed
            dy = math.sin(angle_rad) * JUMP_Speed
            X_POSITION += dx
            Y_POSITION += dy
            frog.rect.centerx = frog.x_pos
            frog.rect.centery = frog.y_pos
            Y_VELOCITY -= Y_GRAVITY

            frog_rect = Frog_j.get_rect(center=(X_POSITION + visual_offset_x, Y_POSITION + visual_offset_y))
            rotated_frog = pygame.transform.rotate(Frog_j, frog_angle)
            Screen.blit(rotated_frog, frog_rect)
            draw_rotated_mask_at_position(screen, X_POSITION, Y_POSITION, frog_angle, frog.hitbox_surface)

            if Y_VELOCITY < -JUMP_HEIGHT:
                jumping = False
                Y_VELOCITY = JUMP_HEIGHT
                frog.jumping = False
                frog.update_image()
        else:
            visual_offset_x = 0
            visual_offset_y = 0
            frog.rect.centerx = X_POSITION + visual_offset_x
            frog.rect.centery = Y_POSITION + visual_offset_y
            frog_rect = Frog_s.get_rect(center=(X_POSITION + visual_offset_x, Y_POSITION + visual_offset_y))
            rotated_frog = pygame.transform.rotate(Frog_s, frog_angle)
            Screen.blit(rotated_frog, frog_rect)
            draw_rotated_mask_at_position(screen, X_POSITION, Y_POSITION, frog_angle, frog.hitbox_surface)

        # Get the hitbox position
        hitbox_rect = frog.get_hitbox_rect()
        # Draw mask at the hitbox position
        #draw_rotated_mask_at_position(screen, hitbox_rect.centerx, hitbox_rect.centery, frog_angle, frog.hitbox_surface)
        frog.update_image()
        print(f"Frog rect: ({frog.rect.x}, {frog.rect.y}), size: {frog.rect.size}")
        print(f"Frog position: ({frog.x_pos}, {frog.y_pos})")
        print(f"Frog hitbox: {frog.get_hitbox_rect()}")

        for petal in petal_group:
            print(f"Petal rect: ({petal.rect.x}, {petal.rect.y}), size: {petal.rect.size}")
            break

        BOTTOM_BOUNDARY = 50
        if Y_POSITION > (SCREEN_HEIGHT) - BOTTOM_BOUNDARY:
            Y_POSITION = ((SCREEN_HEIGHT) - BOTTOM_BOUNDARY)



        if level_completion():
            advance_level(Screen)
            X_POSITION = Initial_X
            Y_POSITION = Initial_Y

        # fall water defineren

        # if outside of map end game
    elif game_over == True:
        GAME_STATE = "GAME_OVER"
        restart_button, main_menu_button = show_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button and restart_button.collidepoint(event.pos):
                    restart_game()
                elif main_menu_button and main_menu_button.collidepoint(event.pos):
                    GAME_STATE = "MENU"
                    X_POSITION = Initial_X
                    Y_POSITION = Initial_Y
                    frog.rect.center = (X_POSITION, Y_POSITION)
                    jumping = False
                    frog.jumping = False

    for petal in petal_group:
        draw_mask(screen, petal, (255, 0, 0))
        draw_rotated_mask_at_position(screen, X_POSITION, Y_POSITION, frog_angle, frog.hitbox_surface)
        hitbox_rect = frog.get_hitbox_rect()

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
