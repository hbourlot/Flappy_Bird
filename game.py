from asyncio import create_task

import pygame
import os
from src.handle_keys import handle_keys
from src.menu import *
from src.player import *
from src.background import *
from src.score import *
from enum import Enum, auto

class GameState(Enum):
    MENU = auto() # 1
    PLAYING = auto() # 2
    GAME_OVER = auto() # 3
    PAUSE = auto() # 4


def main():
    pygame.init()
    pygame.display.set_caption("Flappy Bird :)")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    current_state = GameState.MENU
    dt = 0
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    # Initialize game objects
    background = Background(screen)
    menu = Menu()
    player = Player(screen)
    score = Score(screen)

    def handle_event(event):
        nonlocal running, current_state

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_state == GameState.MENU:
                    current_state = GameState.PLAYING
                elif current_state == GameState.PLAYING:
                    player.flap()
                    score.increment()
            elif event.key == pygame.K_ESCAPE:
                running = False
            # elif event.key == pygame.K_p and current_state == GameState.PLAYING:
            #     current_state = GameState.PAUSE

    while running:
        # Handle events
        for event in pygame.event.get():
            handle_event(event)

        # Update game state
        background.draw()

        if current_state == GameState.MENU:
            menu.draw(screen)
        elif current_state == GameState.PLAYING:
            player.update()
            player.draw()
            score.draw(False, False)
            if not player.alive:
                current_state = GameState.GAME_OVER
                score.reset()
        # elif current_state == GameState.GAME_OVER:
        #     # Add game over screen logic here
        #     pass
        # elif current_state == GameState.PAUSE:
        #     # Add pause screen logic here
        #     pass

        pygame.display.flip()
        dt = clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()