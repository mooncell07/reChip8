import pygame
from .constants import ROWS, COLUMNS, COLORS

pygame.init()


__all__ = ("Display", "ROWS", "COLUMNS")


class Display:
    def __init__(self, screen, multiplier):
        self.screen = screen
        self.multiplier = multiplier
        self.buffer = bytearray(ROWS * COLUMNS)

    @classmethod
    def create(cls, multiplier):
        screen = pygame.display.set_mode((COLUMNS * multiplier, ROWS * multiplier))
        self = cls(screen, multiplier)
        self.clear()

        return self

    def update(self):
        pygame.display.flip()

    def delete(self):
        pygame.quit()
        raise SystemExit

    def wrap(self, x, y):
        x %= COLUMNS
        y %= ROWS

        loc = x + (y * COLUMNS)
        return loc

    def render(self):
        for i in range(ROWS * COLUMNS):
            x = (i % COLUMNS) * self.multiplier
            y = (i // COLUMNS) * self.multiplier

            if self.buffer[i]:
                pygame.draw.rect(
                    self.screen,
                    COLORS["ON"],
                    pygame.Rect(x, y, self.multiplier, self.multiplier),
                )
        self.update()

    def clear(self):
        self.buffer = bytearray(ROWS * COLUMNS)
        self.screen.fill(COLORS["OFF"])
