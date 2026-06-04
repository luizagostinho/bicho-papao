import pygame

from code.const import *

class Background:

    def __init__(self):

        self.bg = pygame.image.load(
            "asset/background.png"
        ).convert()

        self.bg = pygame.transform.scale(
            self.bg,
            (WIN_WIDTH, WIN_HEIGHT)
        )

        self.x = 0

    def draw(self, screen):

        screen.blit(self.bg, (self.x, 0))
        screen.blit(self.bg, (self.x + WIN_WIDTH, 0))

    def update(self, speed):
        self.x -= speed

        if self.x <= -WIN_WIDTH:
            self.x = 0

