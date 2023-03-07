import argparse
import logging
import pygame

from components import CPU, INIT_LOC_CONSTANT, TICK, Display, Keypad, Memory

logging.basicConfig(
    format="%(asctime)s:%(msecs)03d (%(levelname)s/%(module)s): %(message)s",
    level=logging.DEBUG,
    encoding="utf-8",
    datefmt="%M:%S",
)


class Lemon:
    __slots__ = ("FPS", "cpu", "display", "keypad", "memory", "now")

    def __init__(self, rom: str, mul: int) -> None:
        self.memory: Memory = Memory()
        self.load_font()
        self.load_rom(rom)
        self.display: Display = Display.create(multiplier=mul)
        self.keypad: Keypad = Keypad()
        self.cpu: CPU = CPU(
            display=self.display, memory=self.memory, keypad=self.keypad
        )

    def load_font(self) -> None:
        self.memory.load_binary("./bin/FONT")
        logging.info(f"{TICK} Successfully loaded Fontset at location 0x0")

    def load_rom(self, rom: str) -> None:
        self.memory.load_binary(rom, offset=INIT_LOC_CONSTANT)
        logging.info(
            f"{TICK} Successfully loaded ROM at location {hex(INIT_LOC_CONSTANT)}"
        )

    def tick(self) -> None:
        if not self.cpu.halt:
            self.cpu.step()

        self.display.render()

    def run(self) -> None:
        cycle = True
        while cycle:
            self.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cycle = False
                if event.type == pygame.KEYDOWN:
                    if event.key in self.keypad.keymap:
                        self.keypad.set(self.keypad.keymap[event.key])
                if event.type == pygame.KEYUP:
                    if event.key in self.keypad.keymap:
                        self.keypad.unset(self.keypad.keymap[event.key])

        self.display.delete()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Lemon", description="Chip-8 Virtual Machine."
    )
    parser.add_argument("rom", help="Path to the rom file.")
    parser.add_argument(
        "--scale", help="Scale up\down the display window.", type=int, default=10
    )
    args = parser.parse_args()

    lemon = Lemon(args.rom, args.scale)
    lemon.run()
