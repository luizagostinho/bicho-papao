WIN_WIDTH = 576
WIN_HEIGHT = 324   # medidas

MENU = 0
PLAYING = 1
SCORES = 2
GAME_OVER = 3

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

PLAYER_SPEED = 4
GRAVITY = 0.9           # condições pro player
JUMP_FORCE = -14

SPRITE_SIZE = (100, 100)

LEVELS = {
    1: {
        "x": 100,
        "ground_y": 225
    },

    2: {
        "x": 100,
        "ground_y": 240
    },

    3: {
        "x": 100,
        "ground_y": 195
    }
}

BACKGROUNDS = {
    1: "asset/background2.png",
    2: "asset/background3.png",      # fundo das fses
    3: "asset/background4.png",
}

GROUND_Y = {
    1: (100, 200),
    2: (205, 205),
    3: (100, 220),     # bases para spaw do player em cada fase
    4: (120, 210),
}