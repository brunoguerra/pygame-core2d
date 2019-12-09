from core2d import Game, Player, Sprite, Enemy, Stage

class SpacePlayer(Player):
    PLAYER_MOVE_X_RATE = 0.42
    PLAYER_SIZE = 60
    HALF_OF_PLAYER_SIZE = PLAYER_SIZE / 2
    def __init__(self, game):
        super().__init__(game)
        self.playerX = 0
        self.playerY = 0

    def setup(self, player_number=0):
        self.set_image('player.png')
        self.set_number(player_number)
        self.playerX = self.game.get_width() // 2 - SpacePlayer.HALF_OF_PLAYER_SIZE
        self.playerY = self.game.get_height() // 2 + SpacePlayer.PLAYER_SIZE #480
        self.update()
    
    def update(self):
        self.set_location((self.playerX, self.playerY))
        super().update()

    def render(self):
        player_number = self.get_number()
        left_pressed = self.game.is_pressed(player_number, self.game.PLAYER_MOVE_LEFT)
        right_pressed = self.game.is_pressed(player_number, self.game.PLAYER_MOVE_RIGHT)
        if left_pressed:
            if (self.playerX - SpacePlayer.PLAYER_MOVE_X_RATE) > 5:
                self.playerX -= SpacePlayer.PLAYER_MOVE_X_RATE
        elif right_pressed:
            if (self.playerX + SpacePlayer.PLAYER_SIZE + SpacePlayer.PLAYER_MOVE_X_RATE) < self.game.WIDTH - 5:
                self.playerX += SpacePlayer.PLAYER_MOVE_X_RATE
        self.update()

class SpaceBasiceEnemy(Enemy):
    ENEMY_MOVE_X_RATE = 0.04 # power difficulty
    def setup(self):
        self.set_image('enemy.png')

class IntroStage(Stage):
    def setup(self):
        self.set_options({
            'background-color': (30, 70, 140)
        })

class EpicDungeon(Sprite):
    def __init__(self, stage, enemies):
        super().__init__(stage._game)
        self.enemies = enemies

    def update(self):
        pass


class GameStage(Stage):
     def setup(self):
        self.set_options({
            'background-color': (90, 170, 240)
        })
        self.spacePlayer = SpacePlayer(self._game)
        self.add_player(self.spacePlayer)
        self._dungeon = EpicDungeon(self, (SpaceBasiceEnemy))
        self.add_node(self._dungeon)

class GameOverStage(Stage):
    def setup(self):
        self.set_options({
            'background-color': (150, 210, 254)
        })

class SpaceGame(Game):
    def get_stages(self):
        return (
            # IntroStage,
            GameStage,
            GameOverStage,
        )
