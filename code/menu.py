import pygame

from code.const import *

class Menu:

    def __init__(self):

        self.background = pygame.image.load(
            "asset/background.png"
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            (WIN_WIDTH, WIN_HEIGHT)
        )

        self.title_font = pygame.font.Font(
            "asset/fonts/MedievalSharp.ttf",
            48
        )

        self.option_font = pygame.font.Font(
            "asset/fonts/MedievalSharp.ttf",
            28
        )

        self.options = [
            "NEW GAME",
            "SCORES"
        ]

        self.selected = 0

    def draw(self, screen):

        screen.blit(self.background, (0, 0))

        title = self.title_font.render(
            "GHOST DEMO",
            True,
            WHITE
        )

        screen.blit(
            title,
            (
                WIN_WIDTH//2 - title.get_width()//2,
                50
            )
        )

        for i, option in enumerate(self.options):

            color = YELLOW if i == self.selected else WHITE

            text = self.option_font.render(
                option,
                True,
                color
            )

            screen.blit(
                text,
                (
                    WIN_WIDTH//2 - text.get_width()//2,
                    160 + i * 40
                )
            )