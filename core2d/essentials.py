
import pygame
PYGAME_KEY_EVENTS = (pygame.KEYDOWN, pygame.KEYUP)

K_CONFIG = "GAME////CONFIG"
K_CONTROL = "GAME////CONTROL"
K_CONTROL_ACTION_TO_KEY = "GAME////CONTROL////KEY"

class Game:
    """
    Define game object to resolve controller and stages
    This Class define a prototype of game library named core2d
    from \"pygamer\" to \"pygamers\" with love
    """

    PLAYER_MOVE_UP = "GAME////PLAYER////MOVE////UP"
    PLAYER_MOVE_LEFT = "GAME////PLAYER////MOVE////LEFT"
    PLAYER_MOVE_RIGHT = "GAME////PLAYER////MOVE////RIGHT"
    PLAYER_MOVE_DOWN = "GAME////PLAYER////MOVE////DOWN"
    PLAYER_FIRE = "GAME////PLAYER////MOVE////FIRE"

    def __init__(self, size):
        pygame.init()
        self._stages = []
        self.set_size(size)
        self._control = Control(self)
        self._default_stage = None
        for stage in self.get_stages():
            self.add_stage(stage)
        self.WIDTH, self.HEIGHT = size
        
        # Hacking pygame keys definition to into our class
        for key in [k_element for k_element in dir(pygame) if k_element.startswith('K_')]:
            setattr(self, key, getattr(pygame, key))
    
    def set_size(self, size):
        """
        Sets a size for pygame.Screen
        """
        self.size = size
        self.screen = pygame.display.set_mode(size)

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[0]

    def set_display_basis(self, title, icon):
        pygame.display.set_caption(title)
        icon_image = pygame.image.load(icon)
        pygame.display.set_icon(icon_image)

    def add_stage(self, stage):
        self._stages.append(stage)
        if not self._default_stage:
            self.set_default_stage(stage)

    def set_default_stage(self, default_stage):
        self._default_stage = default_stage
        self.set_current_stage(self._default_stage)

    def init(self):
        self._current_stage._setup()
    
    def set_current_stage(self, stage):
        self._current_stage = (stage or self._default_stage)(self)
        self._current_stage._setup()

    def render(self):
        for event in pygame.event.get():
            self.update_cntrls(event)
        if self._control.is_quiting():
            return False
        self._current_stage.before_render()
        self._current_stage.render()
        
        pygame.display.update()
        return True
    
    def update_cntrls(self, event):
        self._control.update(event)
    
    def fill(self, color):
        self.screen.fill(color)

    def set_player_controls(self, player_number, controls):
        self._control.set_player_controls(player_number, controls)

    def is_pressed(self, player_number, player_aciton):
        return self._control.is_pressed(player_number, player_aciton)

class Control:
    def __init__(self, game, watch_keys=()):
        """
        Receive a tuple with keys to watch
        """
        self._game = game
        self._player_defs = {}
        self._running = True
        self._pressed = {}
        self.watching_keys = watch_keys
        self.key_for_players = {}
    
    def update(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type in PYGAME_KEY_EVENTS:
            for key in self.watching_keys:
                if event.key == key:
                    if event.type == pygame.KEYDOWN:
                        self.set_key_pressed(key)
                    elif event.type == pygame.KEYUP:
                        self.set_key_released(key)
    

    def is_quiting(self):
        return not self._running

    def set_player_controls(self, player_number, controls):
        if player_number not in self._player_defs.keys():
            self.setup_player_configs(player_number)
        
        player_config = self._player_defs[player_number][K_CONFIG]
        player_config[K_CONTROL] = controls
        player_config[K_CONTROL_ACTION_TO_KEY] = dict((v,k) for k,v in controls.items())

        keys_to_watch = controls.keys()
        self.add_watch_keys(player_number, keys_to_watch)

    def is_pressed(self, player_number, player_action):
        player_config = self._player_defs[player_number][K_CONFIG]
        key = player_config[K_CONTROL_ACTION_TO_KEY][player_action]
        return self._pressed.get(key)

    def add_watch_keys(self, player_number, keys):
        """
        Append keys for be watched in the game and
        bind to game object
        """
        print('keys', keys)
        self.watching_keys = set(list(keys) + list(self.watching_keys))
        for key in keys:
            if key not in self.key_for_players.keys():
                self.key_for_players[key] = []
            self.key_for_players[key].append(player_number)

    def setup_player_configs(self, player_number):
        dicio = self._player_defs[player_number] = {}
        dicio[K_CONFIG] = {}
    
    def set_key_pressed(self, key):
        self._pressed[key] = True
        # self._game.notify(self.key_for_players[key], {
        #     'type': 'key',
        #     'value': key
        # })

    def set_key_released(self, key):
        self._pressed[key] = False

class Stage:
    def __init__(self, game, nodes=[], options={}):
        """
        Receive game and optional arg options for define
        basis of stage options. Availiable keys:
          * background-color: defines stage background color
        """
        self._game = game
        self._nodes = nodes
        self._current_player = None
        if len(options)>0:
            self.set_options(options)
        self._players = []
        self.already_setuped = False
    
    def set_options(self, options):
        self.bg_color = options.get('background-color')

    def add_node(self, node):
        self._nodes.append(node)

    def _setup(self):
        """
        Abstract method for composite a stage elements
        into the game
        """
        if self.already_setuped:
            return False

        self.set_options({})
        for player in self._players:
            player.setup()
        if 'setup' in dir(self):
            self.setup()

        for player in self._players:
            player.setup()
        self.already_setuped = True

    def before_render(self):
        """
        Called by game as lifecycle callback
        before render
        """
        pass

    def render(self):
        self._game.fill(self.bg_color)
        for node in self._nodes:
            node.before_render()
            node.render()
            if 'nodes' in dir(node):
                for snode in node.nodes:
                    snode.render()
            node.after_render()
    
    def stage_peformed_render(self):
        """
        Called by game as lifecycle callback
        after render
        """
        pass

    def add_player(self, player):
        if self._current_player == None:
            self._current_player = player
            self._current_player_number = len(self._players)
        number = len(self._players)
        self._players.append(player)
        player.set_number(number)
        self.add_node(player)

class Sprite:
    """
    It will render a image and move.
    Represent a composite pattern
    """
    def __init__(self, game):
        self.game = game
        self._location = (0, 0)
        self.has_image = False
    
    def set_location(self, location):
        self._location = location

    def set_image(self, image):
        """
        Receive image as str then locate the file
        and load it with pygame to represent graphical
        element for this instance
        """
        self._image = pygame.image.load(image)
        self.has_image = True

    def before_render(self):
        pass

    def render(self):
        self.update()

    def update(self):
        if self.has_image:
            self.game.screen.blit(self._image, self._location)
        

    def after_render(self):
        pass

class Player(Sprite):
    """
    It could be controlled by keys and
    played as main actor.
    """

    def set_number(self, number):
        self._player_number = number
    
    def get_number(self):
        return self._player_number

class Enemy(Sprite):
    """
    It could be controlled by keys and
    played as main actor.
    """

"""
Author: Bruno Guerra
Github: github.com/brunoguerra/pygame-core2d.git
"""