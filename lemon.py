import argparse
import logging
import logging.config

import pygame

from components import CPU, INIT_LOC_CONSTANT, Display, Memory, TICK

logging.config.fileConfig("journal.conf")
logger = logging.getLogger(__name__)


class Lemon:
    def __init__(self, rom) -> None:
        self.memory = Memory()
        self.load_rom(rom)

        self.display = Display.create(multiplier=15)
        self.cpu = CPU(logger, display=self.display, memory=self.memory)

    def load_font(self):
        self.memory.load_binary("./bin/FONT")

    def load_rom(self, rom):
        self.memory.load_binary(rom, offset=INIT_LOC_CONSTANT)
        logger.info(f"{TICK} ROM loaded at {hex(INIT_LOC_CONSTANT)}")

    def boot(self):
        self.load_font()
        cycle = True

        while cycle:
            self.cpu.step()
            self.display.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cycle = False

        self.display.delete()


parser = argparse.ArgumentParser(prog="Lemon", description="Chip-8 Virtual Machine.")
parser.add_argument("rom", help="Path to the rom file.")
args = parser.parse_args()

lemon = Lemon(args.rom)
lemon.boot()
