import pygame

from code.const import *

class ScoreScreen:

    def __init__(self):

        self.font = pygame.font.SysFont(
            "Arial",
            28
        )

    def draw(self, screen):

        screen.fill((0,0,0))

        title = self.font.render(
            "HIGH SCORES",
            True,
            WHITE
        )

        screen.blit(title, (180, 50))

        scores = [
            "1. 12000",
            "2. 8000",
            "3. 5000"
        ]

        for i, score in enumerate(scores):

            text = self.font.render(
                score,
                True,
                WHITE
            )

            screen.blit(
                text,
                (220, 120 + i * 40)
            )