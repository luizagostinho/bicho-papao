import pygame

from code.player import Player
from code.enemy import Zombie
from code.background import Background


class Game:

    def __init__(self, screen):

        self.screen = screen

        self.player = Player()

        self.zombie = Zombie()

        self.background = Background()

    def run(self):

        self.player.move()

        self.player.update()

        # attack_rect = self.player.get_attack_rect()
        #
        # if attack_rect:
        #
        #     if self.zombie.alive:
        #
        #         if attack_rect.colliderect(
        #             self.zombie.rect
        #         ):
        #
        #             self.zombie.alive = False

        self.background.draw(self.screen)

        self.player.draw(self.screen)
        self.zombie.draw(
            self.screen
        )

        # if attack_rect:
        #
        #     pygame.draw.rect(
        #         self.screen,
        #         (255, 0, 0),
        #         attack_rect
        #     )