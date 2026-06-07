import random
import pygame

from code.const import LEVELS, BACKGROUNDS, WIN_WIDTH
from code.player import Player
from code.enemy import Zombie, Morcego
from code.enemy import Zombie, Morcego, Boss


class Game:

    def __init__(self, screen):
        self.game_over = False
        self.hp = 3
        self.transition_cooldown = 0
        self.boss_spawned = False
        self.screen = screen
        self.level = 1
        self.player = Player(LEVELS[1]["ground_y"])
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_delay = 120
        self.font = pygame.font.SysFont(None, 24)
        self.backgrounds = {}

        for level, path in BACKGROUNDS.items():
            bg = pygame.image.load(path).convert()

            bg = pygame.transform.scale(
                bg,
                (self.screen.get_width(), self.screen.get_height())
            )

            self.backgrounds[level] = bg

    def spawn_enemy(self):

        # Fase do boss
        if self.level == len(LEVELS):
            if not self.boss_spawned:
                self.enemies.clear()
                self.enemies.append(
                    Boss(
                        350,
                        100
                    )
                )
                self.boss_spawned = True
            return

        # Fases normais
        enemy_type = random.choice(
            ["zombie", "morcego"]
        )

        if enemy_type == "zombie":
            self.enemies.append(
                Zombie(
                    WIN_WIDTH + 50,
                    LEVELS[self.level]["ground_y"]
                )
            )

        else:

            player_chest = self.player.rect.y - 40
            jump_top = self.player.rect.y - 80
            bat_y = random.randint(
                jump_top + 10,
                player_chest
            )

            self.enemies.append(
                Morcego(
                    WIN_WIDTH + 50,
                    bat_y
                )
            )

    def run(self):
        if self.game_over:
            bg = pygame.image.load(
                "asset/gameover.png"
            ).convert()

            bg = pygame.transform.scale(
                bg,
                (576, 324)
            )

            self.screen.blit(bg, (0, 0))

            font = pygame.font.SysFont(None, 32)

            text = font.render(
                "Pressione ENTER",
                True,
                (255, 255, 255)
            )

            self.screen.blit(text, (180, 280))

            return

        attack_rect = self.player.get_attack_rect()

        if attack_rect:

            for enemy in self.enemies[:]:

                if attack_rect.colliderect(enemy.rect):
                    self.enemies.remove(enemy)
        
                
        attack_rect = self.player.get_attack_rect()

        if attack_rect:
            pygame.draw.rect(
                self.screen,
                (255, 255, 0),
                attack_rect,
                2
            )
            


        attack_rect = self.player.get_attack_rect()

        if attack_rect:

            for enemy in self.enemies[:]:

                if attack_rect.colliderect(enemy.rect):

                    if not self.player.attack_hit:

                        enemy.hp -= 1

                        self.player.attack_hit = True

                        enemy.damage_cooldown = 30  # meio segundo

                        print(f"Boss HP: {enemy.hp}")

                        if enemy.hp <= 0:
                                self.enemies.remove(enemy)

                                print("VOCÊ VENCEU!")
                    else:

                        self.enemies.remove(enemy)
        for enemy in self.enemies:

            if self.player.rect.colliderect(enemy.rect):

                if self.player.invincible <= 0:

                    self.player.lives -= 1

                    self.player.invincible = 120

                    if self.player.lives <= 0:
                        self.game_over = True

                        pygame.mixer.music.stop()

                        pygame.mixer.music.load(
                            "asset/gameover.mp3"
                        )

                        pygame.mixer.music.play()


        if self.transition_cooldown > 0:
            self.transition_cooldown -= 1
        if self.level == 1:
            self.spawn_delay = 120
        elif self.level == 2:
            self.spawn_delay = 90
        elif self.level == 3:
            self.spawn_delay = 60
        elif self.level == 4:
            self.spawn_delay = 45
        self.spawn_timer += 1
        if self.level < len(LEVELS) and self.spawn_timer >= self.spawn_delay:
            self.spawn_enemy()
            self.spawn_timer = 0

        ground_y = LEVELS[self.level]["ground_y"]
        self.player.move()
        self.player.update(ground_y)

        # Fase 1: bloqueia esquerda
        if self.level == 1 and self.player.rect.left < 0:
            self.player.rect.left = 0

        # Última fase: bloqueia direita
        if self.level == len(LEVELS) and self.player.rect.right > WIN_WIDTH:
            self.player.rect.right = WIN_WIDTH

        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.rect.right < 0:
                self.enemies.remove(enemy)

        # Voltar de fase
        if self.player.rect.left <= 0 and self.level > 1 and self.level < len(LEVELS):
            self.level -= 1
            self.player.rect.right = WIN_WIDTH - 10
            self.player.rect.y = LEVELS[self.level]["ground_y"]
            self.player.vel_y = 0
            print("Nível antes:", self.level)
        # Avançar de fase
        elif (
                self.player.rect.right >= WIN_WIDTH
                and self.level < len(LEVELS)
                and self.transition_cooldown == 0
        ):
            self.level += 1
            self.player.rect.left = 10
            self.player.rect.y = LEVELS[self.level]["ground_y"]
            self.player.vel_y = 0

            self.transition_cooldown = 30

            if self.level == len(LEVELS):
                self.spawn_enemy()

            self.player.rect.left = 10
            self.player.rect.y = LEVELS[self.level]["ground_y"]
            self.player.vel_y = 0

        # Parede esquerda da fase 1
        if self.level == 1 and self.player.rect.left < 0:
            self.player.rect.left = 0

        # Parede direita da última fase
        if self.level == len(LEVELS) and self.player.rect.right > WIN_WIDTH:
            self.player.rect.right = WIN_WIDTH

        self.draw_background()
        self.draw_background()

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen)

        vidas_text = self.font.render(
            f"Vidas: {self.player.lives}",
            True,
            (255, 0, 0)
        )

        self.screen.blit(
            vidas_text,
            (10, 40)
        )

        for enemy in self.enemies:

            enemy.draw(self.screen)

        self.player.draw(self.screen)

        text = self.font.render(
            f"Nivel: {self.level}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(text, (10, 10))

    def draw_background(self):

        self.screen.blit(
            self.backgrounds[self.level],
            (0, 0)
        )

