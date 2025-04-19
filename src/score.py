from configs import *
from src.utils import  *
from typing import List
from pygame import mixer
from src.background import *
import os


class Score:
    def __init__(self, screen):
        self.digits = [None] * 10
        self.number = 48
        self.screen = screen
        self.digit_width = 24
        self.position = (SCREEN_WIDTH // 2, 50) # HELP HERE
        self.current_score = 0
        self.load_digit_sprites()

    def load_digit_sprites(self):
        for i in range(10):
            # Convert ASCII code to character
            num_char = chr(self.number)
            self.digits[i] = create_sprite(SPRITE_PATH, f"%c.png" % num_char)
            self.number += 1

    def increment(self, pipes: List[PipePair], player_pos: Vector2):

        for pipe in pipes:
            pipe_right_edge = pipe.pos_x + pipe.width
            if not pipe.scored and pipe_right_edge < player_pos.x:
                self.current_score += 1
                pipe.scored = True
                self.audio()

    def reset(self):
        """Reset score to 0"""
        self.current_score = 0

    def draw(self, current_state: GameState):
        """Draw the current score on screen"""
        if current_state == GameState.PLAYING or current_state == GameState.GAME_OVER:
            score_str = str(self.current_score)
            total_width = len(score_str) * self.digit_width

            # Calculate starting position (centered)
            start_x = self.position[0] - (total_width // 2)

            for i, digit in enumerate(score_str):
                digit_sprite = self.digits[int(digit)]
                if digit_sprite:
                    # Position digits side by side
                    x_pos = start_x + (i * self.digit_width)
                    self.screen.blit(digit_sprite, (x_pos, self.position[1]))

    @staticmethod
    def audio() -> None:
        mixer.music.load(os.path.join(AUDIO_PATH, "point.wav"))
        mixer.music.play()