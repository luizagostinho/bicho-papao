import pygame

from code.const import *
from code.menu import Menu
from code.game import Game

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Bicho Papão")

clock = pygame.time.Clock()

# estados
MENU = 0
PLAYING = 1
SCORES = 2

state = MENU

menu = Menu(screen)
game = Game(screen)

pygame.mixer.music.load("asset/music.mp3")
pygame.mixer.music.play(-1)

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ================= MENU =================
        if state == MENU:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    menu.selected -= 1

                if event.key == pygame.K_DOWN:
                    menu.selected += 1

                menu.selected %= len(menu.options)

                if event.key == pygame.K_RETURN:

                    if menu.selected == 0:
                        state = PLAYING

                    elif menu.selected == 1:
                        state = SCORES

        # ================= GAME =================
        elif state == PLAYING:

            if game.game_state == "game_over":

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:

                        game = Game(screen)
                        state = MENU

                        pygame.mixer.music.load("asset/music.mp3")
                        pygame.mixer.music.play(-1)

    # ================= UPDATE / DRAW =================

    if state == MENU:
        menu.run()

    elif state == PLAYING:
        game.run()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()