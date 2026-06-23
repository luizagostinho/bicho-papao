import random
import pygame

from code.const import LEVELS, BACKGROUNDS, WIN_WIDTH
from code.player import Player
from code.enemy import Zombie, Morcego, Boss


class Game:

    def __init__(self, screen):
        self.screen = screen

        # estado do jogo
        self.game_state = "playing"
        self.music_played = False


        # game over
        self.game_over_sound = pygame.mixer.Sound("asset/gameover.mp3")
        self.gameover_played = False

        # vitória
        self.victory_bg = pygame.image.load("asset/victory.png").convert()
        self.victory_bg = pygame.transform.scale(self.victory_bg, (576, 324))

        self.font_big = pygame.font.SysFont(None, 40)
        self.font_small = pygame.font.SysFont(None, 24)
        self.font = pygame.font.SysFont(None, 24)

        # 🎮 mundo
        self.level = 1
        self.player = Player(LEVELS[self.level]["ground_y"])
        self.enemies = []

        self.spawn_timer = 0
        self.spawn_delay = 120
        self.transition_cooldown = 0
        self.boss_spawned = False

        # background
        self.backgrounds = {}
        for lvl, path in BACKGROUNDS.items():
            bg = pygame.image.load(path).convert()
            bg = pygame.transform.scale(bg, (576, 324))
            self.backgrounds[lvl] = bg

    # =========================
    # INIMIGOS
    # =========================
    def spawn_enemy(self):

        if self.level == len(LEVELS):
            if not self.boss_spawned:
                self.enemies.clear()
                self.enemies.append(Boss(350, 100))
                self.boss_spawned = True
            return

        enemy_type = random.choice(["zombie", "morcego"])

        if enemy_type == "zombie":
            self.enemies.append(
                Zombie(WIN_WIDTH + 50, LEVELS[self.level]["ground_y"])
            )
        else:
            y = random.randint(
                self.player.rect.y - 80,
                self.player.rect.y - 40
            )

            self.enemies.append(Morcego(WIN_WIDTH + 50, y))

    # =========================
    # GAME STATES
    # =========================
    def draw_game_over(self):
        if not self.gameover_played:
            self.game_over_sound.play()
            self.gameover_played = True

        bg = pygame.image.load("asset/gameover.png").convert()
        bg = pygame.transform.scale(bg, (576, 324))
        self.screen.blit(bg, (0, 0))

        text = self.font.render("Pressione ENTER", True, (255, 255, 255))
        self.screen.blit(text, (180, 280))

    def draw_victory(self):
        # fundo da tela
        self.screen.blit(self.victory_bg, (0, 0))

        # encontrar o boss na lista de inimigos
        boss = None
        for enemy in self.enemies:
            if hasattr(enemy, 'hp'):
                boss = enemy
                break

        if boss:
            # Exibir HP do boss como texto
            hp_text = self.font_big.render(f"HP Boss: {boss.hp}", True, (255, 255, 255))
            self.screen.blit(hp_text, (230, 150))  # Ajuste a posição conforme o layout

        # Texto para pressionar ENTER
        sub = self.font_small.render(
            "Pressione ENTER para voltar ao menu",
            True,
            (255, 255, 255)
        )
        self.screen.blit(sub, (90, 190))


    # =========================
    # MAIN LOOP
    # =========================
    def run(self):
        if self.game_state == "game_over":
            self.draw_game_over()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.game_state = "menu"
            return

        if self.game_state == "victory":
            self.draw_victory()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.game_state = "menu"
            return

        if not self.music_played:
            pygame.mixer.music.load("asset/music1.mp3")
            pygame.mixer.music.play(-1)
            self.music_played = True

        # loop normal do jogo, enquanto está no estado "playing"
        self.player.attack_hit = False

        # lógica de ataque, spawn, inimigos, etc.
        attack_rect = self.player.get_attack_rect()
        if attack_rect:
            for enemy in self.enemies[:]:
                if attack_rect.colliderect(enemy.rect):
                    if not self.player.attack_hit:
                        if hasattr(enemy, "take_damage"):
                            enemy.take_damage(1)
                        else:
                            self.enemies.remove(enemy)
                        self.player.attack_hit = True
                        break

        # lógica de spawn
        if self.transition_cooldown > 0:
            self.transition_cooldown -= 1

        self.spawn_timer += 1
        if self.level < len(LEVELS) and self.spawn_timer >= self.spawn_delay:
            self.spawn_enemy()
            self.spawn_timer = 0

        # ajuste do tempo de spawn
        self.spawn_delay = {
            1: 120,
            2: 90,
            3: 60,
            4: 45
        }.get(self.level, 120)

        # Atualiza o player
        ground_y = LEVELS[self.level]["ground_y"]
        self.player.move()
        self.player.update(ground_y)

        # Atualiza inimigos
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.rect.right < 0:
                self.enemies.remove(enemy)

        # Verifica dano ao player
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                if self.player.invincible <= 0:
                    self.player.lives -= 1
                    self.player.invincible = 120  # tempo de invencibilidade após dano
                    if self.player.lives <= 0:
                        self.game_state = "game_over"

        # Transição entre fases
        if self.player.rect.right >= WIN_WIDTH and self.transition_cooldown == 0:
            self.level += 1
            self.transition_cooldown = 30
            self.player.rect.left = 10
            self.player.rect.y = LEVELS[self.level]["ground_y"]
            self.player.vel_y = 0

            if self.level == len(LEVELS):
                self.spawn_enemy()

        # Verifica se o boss foi derrotado
        for enemy in self.enemies[:]:
            if hasattr(enemy, "hp") and enemy.hp <= 0:
                self.enemies.remove(enemy)
                self.game_state = "victory"

        # Desenha o fundo
        self.draw_background()

        # Desenha inimigos
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Desenha o player
        self.player.draw(self.screen)

        # HUD: mostra vida do player
        self.screen.blit(
            self.font.render(f"Vidas: {self.player.lives}", True, (255, 0, 0)),
            (10, 40)
        )

        # HUD: mostra nível atual
        self.screen.blit(
            self.font.render(f"Nível: {self.level}", True, (255, 255, 255)),
            (10, 10)
        )

    # =========================
    # BACKGROUND
    # =========================
    def draw_background(self):
        self.screen.blit(self.backgrounds[self.level], (0, 0))