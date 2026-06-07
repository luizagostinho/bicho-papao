import pygame
from code.const import SPRITE_SIZE


class Enemy:

    def __init__(self, image_path, x, y, speed, size=None):

        self.image = pygame.image.load(
            image_path
        ).convert_alpha()

        if size is not None:

            self.image = pygame.transform.scale(
                self.image,
                size
            )

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Zombie(Enemy):

    def __init__(self, x, y):

        super().__init__(
            "asset/zombie.png",
            x,
            y,
            1,
            (45, 45)
        )

        self.image = pygame.transform.flip(
            self.image,
            True,
            False
        )


class Morcego(Enemy):

    def __init__(self, x, y):

        super().__init__(
            "asset/morcego.png",
            x,
            y,
            2,
            (50, 15)
        )

class Boss(Enemy):

    def __init__(self, x, y):
        super().__init__(
            "asset/final_boss.png",
            x,
            y,
            0,
            (138, 138)
        )

        self.hp = 15
        self.max_hp = 15
        self.damage_cooldown = 0
        self.direction = -1

        self.rect = self.image.get_rect(topleft=(x, y))

    def take_damage(self, dmg):
        if self.damage_cooldown == 0:
            self.hp -= dmg
            self.damage_cooldown = 20  # invencibilidade curta

    def update(self):

        # cooldown do dano
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        # movimento simples esquerda/direita
        self.rect.x += self.direction

        if self.rect.left <= 300:
            self.direction = 1

        if self.rect.right >= 560:
            self.direction = -1

    def is_dead(self):
        return self.hp <= 0