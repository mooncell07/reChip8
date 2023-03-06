import argparse
import logging
import time
import pygame

from components import CPU, INIT_LOC_CONSTANT, TICK, Display, Memory, Keypad

logging.basicConfig(
    format="%(asctime)s:%(msecs)03d (%(levelname)s/%(module)s): %(message)s",
    level=logging.DEBUG,
    encoding="utf-8",
    datefmt="%M:%S",
)


class Lemon:
    def __init__(self, rom) -> None:
        self.memory = Memory()
        self.load_rom(rom)

        self.display = Display.create(multiplier=15)
        self.keypad = Keypad()
        self.cpu = CPU(display=self.display, memory=self.memory, keypad=self.keypad)
        self.FPS = 60
        self.now = time.time()

    def load_font(self):
        self.memory.load_binary("./bin/FONT")
        logging.info(f"{TICK} Successfully loaded Fontset at location 0x0")

    def load_rom(self, rom):
        self.memory.load_binary(rom, offset=INIT_LOC_CONSTANT)
        logging.info(
            f"{TICK} Successfully loaded ROM at location {hex(INIT_LOC_CONSTANT)}"
        )

    def tick(self):
        self.cpu.step()
        self.display.render()

    def run(self):
        self.load_font()
        cycle = True
        while cycle:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cycle = False
                if event.type == pygame.KEYDOWN:
                    if event.key in self.keypad.keymap:
                        self.keypad.set(self.keypad.keymap[event.key])
                if event.type == pygame.KEYUP:
                    if event.key in self.keypad.keymap:
                        self.keypad.unset(self.keypad.keymap[event.key])
            self.tick()
        self.display.delete()


parser = argparse.ArgumentParser(prog="Lemon", description="Chip-8 Virtual Machine.")
parser.add_argument("rom", help="Path to the rom file.")
args = parser.parse_args()

lemon = Lemon(args.rom)
lemon.run()
