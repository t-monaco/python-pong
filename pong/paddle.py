import pygame


class Paddle:
    VEL = 4
    WIDTH = 20
    HEIGHT = 100
    COLOR = (255, 255, 255)

    def __init__(self, x: int, y: int):
        self.x = self.original_x = x
        self.y = self.original_y = y

    def draw(self, win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.WIDTH, self.HEIGHT))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_y
        self.y = self.original_y
