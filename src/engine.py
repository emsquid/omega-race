import pygame
from random import randrange
from src.base import Object, Explosion, Text
from src.graphics import ForceField
from src.sprites import Player, DroidShip, CommandShip, DeathShip


class Engine:
    def __init__(self):
        self.player = Player()
        self.enemies = (
            [DroidShip(randrange(200, 800), randrange(550, 750)) for i in range(4)]
            + [CommandShip(randrange(200, 800), randrange(550, 750)) for i in range(2)]
            + [DeathShip(randrange(200, 800), randrange(550, 750)) for i in range(1)]
        )
        self.mines = []
        self.player_lasers = []
        self.enemies_lasers = []
        self.explosions = []

        self.force_field = ForceField()

    def get_objects(self) -> list[Object]:
        score_text = Text("SCORE", 330, 330)
        score = Text(str(self.player.score), 330, 350)
        return [
            self.player,
            *self.enemies,
            *self.mines,
            *self.player_lasers,
            *self.enemies_lasers,
            *self.explosions,
            self.force_field,
            score_text,
            score,
        ]

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player.rotating = "left"
            elif event.key == pygame.K_RIGHT:
                self.player.rotating = "right"
            elif event.key == pygame.K_UP and self.player.can_thrust():
                self.player.thrust()
            elif event.key == pygame.K_SPACE and self.player.can_shoot():
                self.player.shoot(self.player_lasers)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.player.rotating == "left":
                self.player.rotating = ""
            elif event.key == pygame.K_RIGHT and self.player.rotating == "right":
                self.player.rotating = ""

    def update(self, dt: int):
        # TODO: Improve that
        self.player.move(dt)

        for enemy in self.enemies:
            enemy.move(dt)
            if self.player.collide(enemy):
                self.player.killed()
                self.explosions.append(Explosion(enemy.x, enemy.y))
                self.enemies.remove(enemy)
            if isinstance(enemy, CommandShip) and enemy.can_shoot():
                enemy.shoot(self.player, self.enemies_lasers)
            if isinstance(enemy, (CommandShip, DeathShip)) and enemy.can_drop():
                enemy.drop_mine(self.mines)

        for mine in self.mines:
            if self.player.collide(mine):
                self.player.killed()
                self.explosions.append(Explosion(mine.x, mine.y))
                self.mines.remove(mine)

        for laser in self.player_lasers:
            laser.move(dt)
            for enemy in self.enemies + self.mines:
                if laser.collide(enemy):
                    self.player.kill(enemy)
                    self.explosions.append(Explosion(enemy.x, enemy.y))
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    else:
                        self.mines.remove(enemy)
                    self.player_lasers.remove(laser)
                    break

        for laser in self.enemies_lasers:
            laser.move(dt)
            if laser.collide(self.player):
                self.player.killed()
                self.explosions.append(Explosion(self.player.x, self.player.y))
                self.enemies_lasers.remove(laser)

        for explosion in self.explosions:
            if explosion.done:
                self.explosions.remove(explosion)

        self.force_field.bounce([self.player, *self.enemies])
        self.force_field.crash(self.player_lasers)
        self.force_field.crash(self.enemies_lasers)
