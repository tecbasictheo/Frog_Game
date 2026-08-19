import pygame
import frog.py
#import helper.py as helper
from random import randint
#
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = ("light blue")
run = True

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Frog Game")

#main game loop -> how to get everything in here
while run:

# call menu
# -> which calls the other game
    #quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()