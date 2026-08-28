import pygame

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOTTOM_BOUNDARY = 50
Screen = pygame.display.set_mode((800, 800))
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
Initial_Y = 750


frog_group = pygame.sprite.Group()
frog = Frog(Initial_X, Initial_Y)
petal_group = pygame.sprite.Group()
for i in range(2):
    new_petal = Petal()
    petal_group.add(new_petal)

class Direction(Enum):
    UP = 0
    DOWN = 180
    LEFT = 270
    RIGHT = 90

#Importet from helper
def show_game_over_screen():
    Screen.fill((255,255,255))
    font = pygame.font.Font(None, 72)  # Large font
    text = font.render("You died", True, (255, 0, 0))  # Red text
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    Screen.blit(text, text_rect)

    #restart button, function testing:
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

# main game loop -> how to get everything in here
while run:
    clock.tick(60)

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
