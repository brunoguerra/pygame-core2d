from space_game import SpaceGame

WIDTH = 800
HEIGHT = 600

def main():
    running = True

    game = SpaceGame((WIDTH, HEIGHT))
    # Set caption name
    game.set_display_basis(
        title='Pylamander Multiplayer',
        icon='salamander.png'
    )

    game.set_player_controls(0, {
        game.K_UP: game.PLAYER_MOVE_UP,
        game.K_LEFT: game.PLAYER_MOVE_LEFT,
        game.K_RIGHT: game.PLAYER_MOVE_RIGHT,
        game.K_DOWN: game.PLAYER_MOVE_DOWN,
        game.K_SPACE: game.PLAYER_FIRE,
    })
    
    game.init()
    
    running = True
    while running:
        running = game.render()
        
            
        

main()