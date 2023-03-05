import pygame as pg

__all__ = ("Keypad",)


class Keypad:
    def __init__(self) -> None:
        self.state = [0] * 17
        self.keys = {}

    @property
    def keymap(self):
        return {
            pg.K_1: 1,
            pg.K_2: 2,
            pg.K_3: 3,
            pg.K_4: 4,
            pg.K_q: 5,
            pg.K_w: 6,
            pg.K_e: 7,
            pg.K_r: 8,
            pg.K_a: 9,
            pg.K_s: 10,
            pg.K_d: 11,
            pg.K_f: 12,
            pg.K_z: 13,
            pg.K_x: 14,
            pg.K_c: 15,
            pg.K_v: 16,
        }

    def set(self, index):
        self.state[index] = 1

    def unset(self, index):
        self.state[index] = 0
