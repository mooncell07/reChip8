from .display import COLUMNS, ROWS
from .opcode import Opcode
from .constants import INIT_LOC_CONSTANT, CROSS
import logging
from tabulate import tabulate

__all__ = ("CPU", "INIT_LOC_CONSTANT")


class CPU:
    def __init__(self, display, memory) -> None:
        self.display = display
        self.memory = memory

        self.V = [0] * 16
        self.I = 0
        self.DT = 0
        self.ST = 0
        self.PC = INIT_LOC_CONSTANT
        self.SP = 0
        self.stack = [0] * 16
        self.PC_inc = True

    def SYS_addr(self, opcode) -> None:
        optab = {0x00: self.NOP, 0xE0: self.CLS}
        optab[opcode.kk](opcode)

    def NOP(self, _) -> None:
        ...

    def CLS(self, _) -> None:
        self.display.clear()

    def JP_addr(self, opcode) -> None:
        self.PC = opcode.nnn
        self.PC_inc = False

    def LD_Vx_byte(self, opcode) -> None:
        self.V[opcode.x] = opcode.kk

    def ADD_Vx_byte(self, opcode) -> None:
        self.V[opcode.x] += opcode.kk
        self.V[opcode.x] &= 0xFF

    def LD_I_addr(self, opcode) -> None:
        self.I = opcode.nnn

    def DRW_Vx_Vy_nibble(self, opcode):
        x = self.V[opcode.x] % COLUMNS
        y = self.V[opcode.y] % ROWS

        self.V[0xF] = 0

        for i in range(opcode.n):
            sprite = self.memory.space[self.I + i]
            for j in range(8):
                px = (sprite >> (7 - j)) & 1
                index = self.display.wrap(x + j, y + i)

                if px == 1 and self.display.buffer[index] == 1:
                    self.V[0xF] = 1

                self.display.buffer[index] ^= px

    @property
    def optable(self):
        return {
            0x0000: self.SYS_addr,
            0x00E0: self.CLS,
            0x1000: self.JP_addr,
            0x6000: self.LD_Vx_byte,
            0x7000: self.ADD_Vx_byte,
            0xA000: self.LD_I_addr,
            0xD000: self.DRW_Vx_Vy_nibble,
        }

    def step(self):
        fetch = (self.memory.space[self.PC] << 8) | self.memory.space[self.PC + 1]
        opcode = Opcode(fetch)
        try:
            operation = self.optable[opcode.type]
        except KeyError:
            logging.error(f"{CROSS} Opcode not found: {opcode}")
            self.display.delete()

        self._log_state(operation, opcode)
        operation(opcode)

        self._ifpcinc()

    def _log_state(self, operation, opcode):
        table = tabulate(
            (
                ("Op", f"{operation.__name__}({opcode})"),
                ("PC", hex(self.PC)),
                ("I", hex(self.I)),
            ),
            headers=("Variable", "Value"),
            tablefmt="github",
        )
        logging.debug(f"\n{table}\n")

    def _ifpcinc(self):
        if self.PC_inc:
            self.PC += 2
        else:
            self.PC_inc = True
