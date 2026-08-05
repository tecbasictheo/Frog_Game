# Class: Petals
# Child classes
# work with lanes

import random
import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 300
BACKGROUND_COLOR = ("light blue")
petal_group = pygame.sprite.Group()

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Petals moving')


class Petal(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("media/Petal1_y.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - 50)
        self.rect.y = 100
        self.speed = 2 #random.randint(1, 2)

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:
            self.rect.x = -200



clock = pygame.time.Clock()
for i in range(2):
    new_petal = Petal()
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