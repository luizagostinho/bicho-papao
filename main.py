import pygame

from code.const import *
from code.menu import Menu
from code.game import Game

pygame.init()

pygame.mixer.init()

pygame.mixer.music.load(
    "asset/music1.mp3"
)

pygame.mixer.music.play(-1)

screen = pygame.display.set_mode(
    (WIN_WIDTH, WIN_HEIGHT)
)


clock = pygame.time.Clock()

menu = Menu()
game = Game(screen)

state = MENU

running = True

while running:


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if state == MENU:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    menu.selected -= 1

                if event.key == pygame.K_DOWN:
                    menu.selected += 1

                menu.selected %= len(menu.options)

                if event.key == pygame.K_RETURN:

                    if menu.selected == 0:

                        pygame.mixer.music.stop()

                        pygame.mixer.music.load(
                            "asset/music1.mp3"
                        )

                        pygame.mixer.music.play(-1)

                        state = PLAYING

                    elif menu.selected == 1:
                        state = SCORES

    if game.game_over:

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                pygame.mixer.music.stop()

                pygame.mixer.music.load(
                    "asset/music.mp3"
                )

                pygame.mixer.music.play(-1)

                menu = Menu()

                game = Game(screen)

                state = MENU

    if state == MENU:

        menu.draw(screen)

    elif state == PLAYING:

        game.run()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()