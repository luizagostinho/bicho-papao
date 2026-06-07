import pygame
from code.const import *

class Menu:

    def __init__(self, screen):
        self.screen = screen

        self.background = pygame.image.load(
            "asset/background.png"
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            (WIN_WIDTH, WIN_HEIGHT)
        )

        self.options = ["NEW GAME", "SCORES"]
        self.selected = 0

        self.title_font = pygame.font.Font(
            "asset/fonts/MedievalSharp",
            48
        )

        self.option_font = pygame.font.Font(
            "asset/fonts/MedievalSharp",
            28
        )

        self.small_font = pygame.font.SysFont(None, 22)

    def run(self):

        self.screen.blit(self.background, (0, 0))

        title = self.title_font.render(
            "BICHO PAPÃO DEMO",
            True,
            WHITE
        )

        self.screen.blit(
            title,
            (WIN_WIDTH//2 - title.get_width()//2, 50)
        )

        for i, option in enumerate(self.options):

            color = YELLOW if i == self.selected else WHITE

            text = self.option_font.render(option, True, color)

            self.screen.blit(
                text,
                (WIN_WIDTH//2 - text.get_width()//2, 160 + i * 40)
            )

        tutorial = self.small_font.render(
            "A/D - Movimento | SPACE - Pular | J - Ataque",
            True,
            WHITE
        )

        self.screen.blit(
            tutorial,
            (20, WIN_HEIGHT - 25)
        )