"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (200, 230, 245)
COLOR_TEXT = (30, 30, 30)


def draw_scene(surface, balloons):
    surface.fill(COLOR_BG)
    for b in balloons:
        pygame.draw.circle(surface, b.color, (int(b.x), int(b.y)), b.radius)
        pygame.draw.line(surface, (120, 120, 120), (b.x, b.y + b.radius), (b.x, b.y + b.radius + 12), 2)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (180, 40, 40))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)


def draw_legend(surface, font):
    """Small color key so the balloon types are easy to tell apart."""
    from game.balloon import BALLOON_TYPES
    y = surface.get_height() - 28
    x = 10
    for kind, info in BALLOON_TYPES.items():
        pygame.draw.circle(surface, info["color"], (x + 8, y + 10), 8)
        label = f"{kind} {info['points']:+d}"
        draw_text(surface, font, label, (x + 22, y))
        x += 22 + font.size(label)[0] + 18


PLAY_AGAIN_RECT = pygame.Rect(WIDTH // 2 - 90, HEIGHT // 2 + 60, 180, 44)


def draw_game_over(surface, font, score, reason):
    """Dim the scene and show the final score with a Play Again button."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))

    big = pygame.font.SysFont("consolas", 52, bold=True)
    cx = surface.get_width() // 2
    cy = surface.get_height() // 2
    for text, f, color, dy in (
        ("GAME OVER", big, (255, 255, 255), -90),
        (reason, font, (230, 230, 230), -40),
        (f"Final score: {score}", big, (255, 220, 80), 10),
    ):
        surf = f.render(text, True, color)
        surface.blit(surf, surf.get_rect(center=(cx, cy + dy)))

    pygame.draw.rect(surface, (60, 160, 90), PLAY_AGAIN_RECT, border_radius=8)
    label = font.render("Play Again (R)", True, (255, 255, 255))
    surface.blit(label, label.get_rect(center=PLAY_AGAIN_RECT.center))
