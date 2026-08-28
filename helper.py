# Class: Petals
# Child classes
# work with lanes

import random
import pygame
#from frog_game import Screen

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


class PetalSpawner:
    def __init__(self):
        self.petals = []
        self.max_count = 6
        self.count = 0
        self.spawn_delay = 1.5
        self.timer = 0

    def update(self, delta_time):
        for petal in self.petals:
            petal.update(delta_time)
        if self.count < self.max_count:
            self.timer += delta_time
            if self.timer > self.spawn_delay:
                petal = Petal((-32, 250), 1, 40)
                other_turtle = Petal((SCREEN_WIDTH, 210), -1, 40)
                self.petals.append(other_turtle)
                self.petals.append(petal)
                self.count += 1
                self.timer = 0
                if self.count == self.max_count // 2:
                    self.spawn_delay = 2

    def draw(self):
        for petal in self.petals:
            petal.draw()
