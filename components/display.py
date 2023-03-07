import typing as t

import pygame

from .constants import COLORS, COLUMNS, ROWS

pygame.init()

img = pygame.image.load("./assets/lemon.png")
__all__ = ("Display",)


class Display:
    __slots__ = ("buffer", "multiplier", "screen")

    def __init__(self, screen: pygame.Surface, multiplier: int):
        self.screen = screen
        self.multiplier = multiplier
        self.buffer: bytearray = bytearray(ROWS * COLUMNS)

    @classmethod
    def create(cls, multiplier: int) -> t.Self:
        screen = pygame.display.set_mode((COLUMNS * multiplier, ROWS * multiplier))
        pygame.display.set_caption("Lemon")
        pygame.display.set_icon(img)
        self = cls(screen, multiplier)

        return self

    def update(self) -> None:
        pygame.display.flip()

    def delete(self) -> None:
        pygame.quit()
        raise SystemExit

    def wrap(self, x: int, y: int) -> int:
        x %= COLUMNS
        y %= ROWS

        loc = x + (y * COLUMNS)
        return loc

    def render(self) -> None:
        self.screen.fill(COLORS["OFF"])
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

    def clear(self) -> None:
        self.buffer = bytearray(ROWS * COLUMNS)
