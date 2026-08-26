# Class: Petals
# Child classes
# work with lanes

import random
import pygame
#from frog_game import Screen

'''
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = ("light blue")
petal_group = pygame.sprite.Group()

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Petals moving')
'''
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

class Petal(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("media/Petal1_y.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - 50)
        self.rect.y = 100
        self.speed = 2 #random.randint(1, 2)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:
            self.rect.x = -200


def show_game_over_screen():
    Screen.fill((255,255,255))
    font = pygame.font.Font(None, 40)  # Large font
    text = font.render("You died", True, (255, 0, 0))  # Red text
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    Screen.blit(text, text_rect)

    #restart button, function testing:
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 50)
    pygame.draw.rect(Screen, (0, 255, 0), restart_button)  # Green button
    restart_text = font.render("Restart", True, (0, 0, 0))
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    Screen.blit(restart_text, restart_text_rect)

    return restart_button

def restart_game():
    global X_POSITION, Y_POSITION
    run = True



'''
clock = pygame.time.Clock()
for i in range(2):
    new_petal = Petal1()
    petal_group.add(new_petal)

flag = True
while flag:
    clock.tick(90)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    petal_group.update()
    screen.fill(BACKGROUND_COLOR)

    petal_group.draw(screen)
    pygame.display.flip()

pygame.quit()
exit(0)
# if condtion is meet in boundery movw with petal if jump break condition
#
'''