import pygame
import math
import random


class Ball:
    MAX_VEL = 5
    RADIUS = 7
    COLOR = (210, 169, 254)

    def __init__(self, x: int, y: int):
        self.x = self.original_x = x
        self.y = self.original_y = y

        angle = self._get_random_angle(-30, 30, [0])
        position = 1 if random.random() < 0.5 else -1

        self.x_vel = position * abs(math.cos(angle) * self.MAX_VEL)
        self.y_vel = math.sin(angle) * self.MAX_VEL

    def _get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.RADIUS)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

        angle = self._get_random_angle(-30, 30, [0])

        # the -1 is to change the direction, it will got to tha player that just scored.
        self.x_vel = -1 * abs(math.cos(angle) * self.MAX_VEL)
        self.y_vel = math.sin(angle) * self.MAX_VEL
