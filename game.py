from pygame.examples.moveit import GameObject
from pygame import mixer
from src.menu import *
from src.player import *
from src.background import *
from src.score import *
import pygame
import os


def main():
    pygame.init()
    pygame.display.set_caption("Flappy Bird :)")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    current_state = GameState.MENU
    dt = 0

    # Initialize game objects
    background = Background(screen)
    menu = Menu(screen)
    player = Player(screen)
    score = Score(screen)

    def handle_event(_event):
        """
        Handles a single Pygame event and updates the game state accordingly.

        - Quits the game on window close.
        - On SPACE key:
            • From MENU → starts the game.
            • From GAME_OVER → returns to the menu.
            • From PLAYING → makes the player flap and increases the score.
        - On ESCAPE key → exits the game.

        :param _event: A single pygame event object to process.
        """
        nonlocal running, current_state

        if _event.type == pygame.QUIT:
            running = False
        elif _event.type == pygame.KEYDOWN:
            key_actions = {
                pygame.K_SPACE: {
                GameState.MENU: lambda: (background.reset(), score.reset(), player.reset(), set_state(GameState.PLAYING)),
                    GameState.GAME_OVER: lambda: set_state(GameState.MENU),
                    GameState.PLAYING: lambda: (player.flap())
                },
                pygame.K_ESCAPE: lambda: stop_running()
            }

            def set_state(state):
                nonlocal current_state
                current_state = state

            def stop_running():
                nonlocal running
                running = False

            action = key_actions.get(_event.key)
            if callable(action):
                action()
            elif isinstance(action, dict):
                state_action = action.get(current_state)
                if callable(state_action):
                    state_action()

    while running:
        # Handle events
        for event in pygame.event.get():
            handle_event(event)

        background.draw(current_state)
        player.draw(current_state)
        score.draw(current_state)
        score.increment(background.get_pipes, player.player_pos)


        if current_state == GameState.MENU:
            menu.start()
        elif current_state == GameState.GAME_OVER:
            menu.game_over()
        elif current_state == GameState.PLAYING:
            if player.has_died(background.floor.get_height(), background.get_pipes):
                current_state = GameState.GAME_OVER

        pygame.display.flip()
        dt = clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()