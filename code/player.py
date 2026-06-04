import pygame

from code.entity import Entity
from code.const import SPRITE_SIZE, PLAYER_SPEED, GRAVITY, JUMP_FORCE


class Player(Entity):

    def __init__(self):

        super().__init__(
            "asset/player.png",
            100,
            190
        )

        SPRITE_SIZE = (96, 96)

        self.idle = pygame.image.load(
            "asset/player.png"
        ).convert_alpha()

        self.run = pygame.image.load(
            "asset/player_run.png"
        ).convert_alpha()

        self.jump = pygame.image.load(
            "asset/player_jump.png"
        ).convert_alpha()

        self.idle = pygame.transform.scale(
            self.idle,
            SPRITE_SIZE
        )

        self.run = pygame.transform.scale(
            self.run,
            SPRITE_SIZE
        )

        self.jump = pygame.transform.scale(
            self.jump,
            SPRITE_SIZE
        )

        self.image = self.idle

        self.rect = self.image.get_rect()

        self.rect.x = 100
        self.rect.y = 190

        self.speed = PLAYER_SPEED

        self.vel_y = 0

        self.on_ground = False

        self.facing_right = True

    def move(self):

        keys = pygame.key.get_pressed()

        moving = False
        moving_right = False

        if keys[pygame.K_a]:

            self.rect.x -= self.speed

            self.facing_right = False

            moving = True

        if keys[pygame.K_d]:
            moving = True
            moving_right = True

        if keys[pygame.K_SPACE] and self.on_ground:

            self.vel_y = JUMP_FORCE

        if not self.on_ground:

            self.image = self.jump

        elif moving:

            self.image = self.run

        else:

            self.image = self.idle

        if not self.facing_right:

            self.image = pygame.transform.flip(
                self.image,
                True,
                False
            )

        return moving_right

    def update(self):

        self.vel_y += GRAVITY

        self.rect.y += self.vel_y

        if self.rect.y >= 200:

            self.rect.y = 200

            self.vel_y = 0

            self.on_ground = True

        else:

            self.on_ground = False