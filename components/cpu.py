from .display import COLUMNS, ROWS
from .opcode import Opcode
from .constants import INIT_LOC_CONSTANT


__all__ = ("CPU", "INIT_LOC_CONSTANT")


class CPU:
    def __init__(self, logger, display, memory) -> None:
        self.display = display
        self.memory = memory
        self.logger = logger

        self.V = [0] * 16
        self.I = 0
        self.DT = 0
        self.ST = 0
        self.PC = INIT_LOC_CONSTANT
        self.SP = 0
        self.stack = [0] * 16

    def SYS_addr(self, opcode) -> None:
        optab = {0x00: self.NOP, 0xE0: self.CLS}
        optab[opcode.kk](opcode)

    def NOP(self, _) -> None:
        ...

    def CLS(self, opcode) -> None:
        self.display.clear()
        self.logger.debug(f"CLS({opcode}): Cleared the screen")

    def JP_addr(self, opcode) -> None:
        log_pc = hex(self.PC)
        self.PC = opcode.nnn
        self.logger.debug(
            f"Jp_addr({opcode}): PC({log_pc}) set to nnn({hex(opcode.nnn)}) [PC={hex(self.PC)}]"
        )

    def LD_Vx_byte(self, opcode) -> None:
        log_vx = hex(self.V[opcode.x])
        self.V[opcode.x] = opcode.kk
        self.logger.debug(
            f"LD_Vx_byte({opcode}): V[{opcode.x}]({log_vx}) set to {hex(opcode.kk)} [V[{opcode.x}]={hex(self.V[opcode.x])}]"
        )

    def ADD_Vx_byte(self, opcode) -> None:
        log_vx = hex(self.V[opcode.x])
        self.V[opcode.x] += opcode.kk
        self.V[opcode.x] &= 0xFF
        self.logger.debug(
            f"ADD_Vx_byte({opcode}): V[{opcode.x}] set to {log_vx} + {hex(opcode.kk)} [Vx+kk={hex(self.V[opcode.x])}]"
        )

    def LD_I_addr(self, opcode) -> None:
        log_i = hex(self.I)
        self.I = opcode.nnn
        self.logger.debug(
            f"LD_I_addr({opcode}): I({log_i}) set to nnn({hex(opcode.nnn)}) [I={hex(self.I)}]"
        )

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
        self.PC += 2

        try:
            self.optable[opcode.type](opcode)
        except KeyError:
            raise ValueError(f"Opcode not found: {hex(opcode.type)}")
