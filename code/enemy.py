from code.entity import Entity


class Zombie(Entity):

    def __init__(self):

        super().__init__(
            "asset/zombie.png",
            350,
            228
        )

        self.alive = True

    def draw(self, screen):

        if self.alive:

            super().draw(screen)