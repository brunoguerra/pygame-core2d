# pygame-core2d
Base game library for easy starting playing

A *definitive* way to start pygame to _2d games_

A declarative way to jump from configuration to fun with pygame

Start code:
```python
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
            IntroStage,
            GameStage,
            GameOverStage,
        )
```