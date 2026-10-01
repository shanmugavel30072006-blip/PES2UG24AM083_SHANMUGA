"""
GameEngine: owns all balloons, spawns new ones, handles clicks, and runs
the round (3 lives, 30-second timer, game over + restart).

Balloons come in three types (normal / bonus / penalty), see
game/balloon.py.
"""

import random
import time

import pygame

from game.balloon import Balloon, BALLOON_TYPES
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45
STARTING_LIVES = 3
ROUND_SECONDS = 30


class GameEngine:
    def __init__(self):
        self.restart()

    def restart(self):
        """Reset score, lives, timer and balloons for a fresh round."""
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = STARTING_LIVES
        self.round_start = time.monotonic()
        self.time_left = float(ROUND_SECONDS)
        self.game_over = False
        self.end_reason = ""

    def _end_round(self, reason):
        self.game_over = True
        self.end_reason = reason
        self.balloons = []          # stop showing / accepting balloons

    def _spawn_balloon(self):
        radius = random.randint(16, 44)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(1.5, 3.0)
        kinds = list(BALLOON_TYPES)
        weights = [BALLOON_TYPES[k]["weight"] for k in kinds]
        kind = random.choices(kinds, weights=weights)[0]
        self.balloons.append(
            Balloon(x=x, y=-radius, radius=radius, speed=speed, kind=kind)
        )

    def handle_click(self, pos):
        if self.game_over:
            from game import renderer
            if renderer.PLAY_AGAIN_RECT.collidepoint(pos):
                self.restart()
            return
        popped = check_pop(self.balloons, pos)
        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points

    def handle_key(self, key):
        if self.game_over and key in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
            self.restart()

    def update(self):
        if self.game_over:
            return

        elapsed = time.monotonic() - self.round_start
        self.time_left = max(0.0, ROUND_SECONDS - elapsed)
        if self.time_left <= 0:
            self._end_round("Time's up!")
            return

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for b in self.balloons:
            b.update()

        # A balloon that reaches the bottom un-popped costs one life.
        # (Popped balloons are removed on click, so popping never costs a life.)
        missed = [b for b in self.balloons if b.is_past_bottom(HEIGHT)]
        self.balloons = [b for b in self.balloons if not b.is_past_bottom(HEIGHT)]
        self.lives -= len(missed)
        if self.lives <= 0:
            self.lives = 0
            self._end_round("Out of lives!")

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.balloons)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Time: {int(self.time_left + 0.999)}s",
                           (WIDTH // 2 - 45, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (WIDTH - 110, 10))
        renderer.draw_legend(surface, font)
        if self.game_over:
            renderer.draw_game_over(surface, font, self.score, self.end_reason)
