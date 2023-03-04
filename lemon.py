import argparse
import logging

import pygame

from components import CPU, INIT_LOC_CONSTANT, TICK, Display, Memory

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
        self.load_font()

        self.display = Display.create(multiplier=15)
        self.cpu = CPU(display=self.display, memory=self.memory)

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
        cycle = True
        while cycle:
            self.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cycle = False

        self.display.delete()

parser = argparse.ArgumentParser(prog="Lemon", description="Chip-8 Virtual Machine.")
parser.add_argument("rom", help="Path to the rom file.")
args = parser.parse_args()

lemon = Lemon(args.rom)
lemon.run()
