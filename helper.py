# Class: Petals
# Child classes
# work with lanes

import random
import pygame
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 850
LANE_HEIGHT = 170


class Petal(pygame.sprite.Sprite):

    def __init__(self, lane):
        super().__init__()

        self.image = pygame.image.load("media/Petal1_y.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - 50)
        self.rect.y = 100 + (lane_number * LANE_HEIGHT)
        self.speed = 1.5
        self.mask = pygame.mask.from_surface(self.image)
        self.lane = lane_number

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:
            self.rect.x = -200
            self.rect.y = 150 + (self.lane * LANE_HEIGHT)

class PetalSpawner:
    def __init__(self):
        self.petals = []
        self.petals_per_lane = {
            0: 4,
            1: 5,
            2: 6,
            3: 7,
            4: 8,
            5: 2
        }
        self.max_count = 10
        self.count = 0
        self.spawn_delay = 1.5
        self.timer = 0

    def update(self, delta_time):
        for petal in self.petals:
            petal.update(delta_time)

        if self.count < self.max_count:
            self.timer += delta_time
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