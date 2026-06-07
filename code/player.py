import pygame

from code.entity import Entity
from code.const import PLAYER_SPEED, GRAVITY, JUMP_FORCE, LEVELS


class Player(Entity):

    def __init__(self, level_y):
        self.attacking = True
        self.attack_timer = 15
        self.attack_hit = False
        self.lives = 3
        self.invincible = 0

        super().__init__("asset/player.png", LEVELS[1]["x"], level_y)

        sprite_size = (40, 40)

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
            sprite_size
        )

        self.run = pygame.transform.scale(
            self.run,
            sprite_size
        )

        self.jump = pygame.transform.scale(
            self.jump,
            sprite_size
        )

        self.image = self.idle
        self.rect = self.image.get_rect()

        self.rect.x = LEVELS[1]["x"]
        self.rect.y = level_y

        self.speed = PLAYER_SPEED

        self.vel_y = 0

        self.on_ground = True

        self.facing_right = True

    def move(self):

        keys = pygame.key.get_pressed()

        moving = False
        moving_right = False

        if keys[pygame.K_j]:

            if self.attack_timer == 0:
                self.attacking = True

                self.attack_timer = 15

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.facing_right = False
            moving = True

        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.facing_right = True
            moving = True
            moving_right = True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_FORCE
            self.on_ground = False

        if not self.on_ground:
            self.image = self.jump
        elif moving:
            self.image = self.run
        else:
            self.image = self.idle

        return moving_right

    def update(self, ground_y):
        if self.invincible > 0:
            self.invincible -= 1

        else:

            self.invulnerable = False

        self.vel_y += GRAVITY

        self.rect.y += self.vel_y

        if self.rect.y >= ground_y:

            self.rect.y = ground_y

            self.vel_y = 0

            self.on_ground = True

        else:

            self.on_ground = False

        if self.attack_timer > 0:

            self.attack_timer -= 1

        else:

            self.attacking = False

    def get_attack_rect(self):

        if not self.attacking:
            return None

        if self.facing_right:

            return pygame.Rect(
                self.rect.right,
                self.rect.y + 20,
                50,
                40
            )

        else:

            return pygame.Rect(
                self.rect.left - 50,
                self.rect.y + 20,
                50,
                40
            )