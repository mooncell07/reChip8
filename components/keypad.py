import pygame as pg

__all__ = ("Keypad",)


class Keypad:
    __slots__ = ("keys", "state")

    def __init__(self) -> None:
        self.state = [0] * 16
        self.keys = {}

    @property
    def keymap(self):
        return {
            pg.K_1: 1,
            pg.K_2: 2,
            pg.K_3: 3,
            pg.K_4: 12,
            pg.K_q: 4,
            pg.K_w: 5,
            pg.K_e: 6,
            pg.K_r: 13,
            pg.K_a: 7,
            pg.K_s: 8,
            pg.K_d: 9,
            pg.K_f: 14,
            pg.K_z: 10,
            pg.K_x: 0,
            pg.K_c: 11,
            pg.K_v: 15,
        }

    def set(self, index):
        self.state[index] = 1

    def unset(self, index):
        self.state[index] = 0
