import pygame


class Entity:

    def __init__(self, image_path, x, y):

        self.image = pygame.image.load(
            image_path
        ).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 190

    def draw(self, screen):

        screen.blit(
            self.image,
            self.rect
        )