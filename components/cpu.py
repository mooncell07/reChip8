from .display import COLUMNS, ROWS
from .opcode import Opcode
from .constants import INIT_LOC_CONSTANT, CROSS
import logging
from tabulate import tabulate
from random import randint
import pygame

__all__ = ("CPU", "INIT_LOC_CONSTANT")


class CPU:
    def __init__(self, display, memory, keypad) -> None:
        # devices
        self.display = display
        self.memory = memory
        self.keypad = keypad

        # registers
        self.V = [0] * 16
        self.I = 0
        self.DT = 0
        self.ST = 0
        self.PC = INIT_LOC_CONSTANT
        self.stack = [0] * 16

        # flags
        self.halt = False

    def SYS_addr(self, opcode) -> None:
        """
        $0nnn - Jump to a machine code routine at nnn. (Edit: use kk instead)
        """
        optab = {0xE0: self.CLS, 0xEE: self.RET}
        optab[opcode.kk]()

    def CLS(self) -> None:
        """
        $00E0 - Clear the display.
        """
        self.display.clear()

    def RET(self) -> None:
        """
        $00EE - Return from a subroutine.
        """
        self.PC = self.stack.pop()

    def JP_addr(self, opcode: Opcode) -> None:
        """
        $1nnn - Jump to location nnn. (PC = nnn)
        """
        self.PC = opcode.nnn

    def CALL_addr(self, opcode: Opcode) -> None:
        """
        $2nnn - Call subroutine at nnn.
        """
        self.stack.append(self.PC)
        self.PC = opcode.nnn

    def SE_Vx_byte(self, opcode: Opcode) -> None:
        """
        $3xkk - Skip next instruction if Vx = kk.
        """
        if self.V[opcode.x] == opcode.kk:
            self.PC += 2

    def SNE_Vx_byte(self, opcode: Opcode) -> None:
        """
        $4xkk - Skip next instruction if Vx != kk.
        """
        if self.V[opcode.x] != opcode.kk:
            self.PC += 2

    def SE_Vx_Vy(self, opcode: Opcode) -> None:
        """
        $5xy0 - Skip next instruction if Vx = Vy.
        """
        if self.V[opcode.x] == self.V[opcode.y]:
            self.PC += 2

    def LD_Vx_byte(self, opcode: Opcode) -> None:
        """
        $6xkk - Set Vx = kk.
        """
        self.V[opcode.x] = opcode.kk

    def ADD_Vx_byte(self, opcode: Opcode) -> None:
        """
        $7xkk - Set Vx = Vx + kk.
        """
        self.V[opcode.x] += opcode.kk
        self.V[opcode.x] &= 0xFF

    def JP_addr_8(self, opcode: Opcode) -> None:
        """
        $8xyn -  Jump to a machine code routine at n.
        """
        optab = {
            0x0: self.LD_Vx_Vy,
            0x1: self.OR_Vx_Vy,
            0x2: self.AND_Vx_Vy,
            0x3: self.XOR_Vx_Vy,
            0x4: self.ADD_Vx_Vy,
            0x5: self.SUB_Vx_Vy,
            0x6: self.SHR_Vx_Vy,
            0x7: self.SUBN_Vx_Vy,
            0xE: self.SHL_Vx_Vy,
        }
        optab[opcode.n](opcode)

    def LD_Vx_Vy(self, opcode: Opcode) -> None:
        """
        $8xy0 - Set Vx = Vy.
        """
        self.V[opcode.x] = self.V[opcode.y]
        self.V[opcode.x] &= 0xFF

    def OR_Vx_Vy(self, opcode: Opcode) -> None:
        """
        $8xy1 - Set Vx = Vx OR Vy.
        """
        self.V[opcode.x] |= self.V[opcode.y]
        self.V[opcode.x] &= 0xFF

    def AND_Vx_Vy(self, opcode: Opcode) -> None:
        """
        $8xy2 - Set Vx = Vx AND Vy.
        """
        self.V[opcode.x] &= self.V[opcode.y]
        self.V[opcode.x] &= 0xFF

    def XOR_Vx_Vy(self, opcode: Opcode) -> None:
        """
        $8xy3 - Set Vx = Vx XOR Vy.
        """
        self.V[opcode.x] ^= self.V[opcode.y]
        self.V[opcode.x] &= 0xFF

    def ADD_Vx_Vy(self, opcode: Opcode) -> None:
        """
        $8xy4 - Set Vx = Vx + Vy, set VF = carry.
        """
        val = self.V[opcode.x] + self.V[opcode.y]

        if val > 0xFF:
            self.V[0xF] = 1
        else:
            self.V[0xF] = 0

        self.V[opcode.x] = val & 0xFF

    def SUB_Vx_Vy(self, opcode: Opcode) -> None:
        """
        $8xy5 - Set Vx = Vx - Vy, set VF = NOT borrow.
        """
        x = self.V[opcode.x]
        y = self.V[opcode.y]

        if x < y:
            self.V[0xF] = 0
        else:
            self.V[0xF] = 1

        self.V[opcode.x] -= y
        self.V[opcode.x] &= 0xFF

    def SHR_Vx_Vy(self, opcode: Opcode) -> None:
        """
        $8xy6 - Set Vx = Vx SHR 1.
        """
        self.V[0xF] = self.V[opcode.x] & 1
        self.V[opcode.x] = self.V[opcode.x] >> 1
        self.V[opcode.x] &= 0xFF

    def SUBN_Vx_Vy(self, opcode: Opcode) -> None:
        """
        $8xy7 - Set Vx = Vy - Vx, set VF = NOT borrow.
        """
        if self.V[opcode.x] > self.V[opcode.y]:
            self.V[0xF] = 0
        else:
            self.V[0xF] = 1

        self.V[opcode.x] = self.V[opcode.y] - self.V[opcode.x]
        self.V[opcode.x] &= 0xFF

    def SHL_Vx_Vy(self, opcode: Opcode) -> None:
        """
        $8xyE - Set Vx = Vx SHL 1.
        """
        self.V[0xF] = self.V[opcode.x] >> 7
        self.V[opcode.x] = self.V[opcode.x] << 1
        self.V[opcode.x] &= 0xFF

    def SNE_Vx_Vy(self, opcode: Opcode) -> None:
        """
        $9xy0 - Skip next instruction if Vx != Vy.
        """
        if self.V[opcode.x] != self.V[opcode.y]:
            self.PC += 2

    def LD_I_addr(self, opcode: Opcode) -> None:
        """
        $Annn - Set I = nnn.
        """
        self.I = opcode.nnn

    def JP_V0_addr(self, opcode: Opcode) -> None:
        """
        $Bnnn - Jump to location nnn + V0.
        """
        self.PC = opcode.nnn + self.V[0]

    def RND_Vx_byte(self, opcode: Opcode) -> None:
        """
        $Cxkk - Set Vx = random byte AND kk.
        """
        self.V[opcode.x] = randint(0, 0xFF) & opcode.kk

    def DRW_Vx_Vy_nibble(self, opcode: Opcode) -> None:
        """
        $Dxyn - Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision. :)
        """
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

    def Jp_addr_E(self, opcode: Opcode) -> None:
        """
        $Exkk - Jump to a machine code routine at kk.
        """
        optab = {0x9E: self.SKP_Vx, 0xA1: self.SKNP_Vx}
        optab[opcode.kk](opcode)

    def SKP_Vx(self, opcode: Opcode) -> None:
        """
        $Ex9E - Skip next instruction if key with the value of Vx is pressed.
        """
        if self.keypad.state[self.V[opcode.x] & 0xF]:
            self.PC += 2

    def SKNP_Vx(self, opcode: Opcode) -> None:
        """
        $ExA1 - Skip next instruction if key with the value of Vx is not pressed.
        """
        if not self.keypad.state[self.V[opcode.x] & 0xF]:
            self.PC += 2

    def Jp_addr_F(self, opcode: Opcode) -> None:
        """
        $Fxkk - Jump to a machine code routine at kk.
        """
        optab = {
            0x07: self.LD_Vx_DT,
            0x0A: self.LD_Vx_K,
            0x15: self.LD_DT_Vx,
            0x18: self.LD_ST_Vx,
            0x1E: self.ADD_I_Vx,
            0x29: self.LD_F_Vx,
            0x33: self.LD_B_Vx,
            0x55: self.LD_I_Vx,
            0x65: self.LD_Vx_I,
        }
        optab[opcode.kk](opcode)

    def LD_Vx_DT(self, opcode: Opcode) -> None:
        """
        $Fx07 - Set Vx = delay timer value.
        """
        self.V[opcode.x] = self.DT

    def LD_Vx_K(self, opcode: Opcode) -> None:
        """
        $Fx0A - Wait for a key press, store the value of the key in Vx.
        """
        self.halt = True
        while self.halt:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key in self.keypad.keymap:
                    key = self.keypad.keymap[event.key]
                    self.keypad.set(key)

                    self.V[opcode.x] = key

                    self.halt = False

    def LD_DT_Vx(self, opcode: Opcode) -> None:
        """
        $Fx15 - Set delay timer = Vx.
        """
        self.DT = self.V[opcode.x]

    def LD_ST_Vx(self, opcode: Opcode) -> None:
        """
        $Fx18 - Set sound timer = Vx.
        """
        self.ST = self.V[opcode.x]

    def ADD_I_Vx(self, opcode: Opcode) -> None:
        """
        $Fx1E - Set I = I + Vx.
        """
        self.I += self.V[opcode.x]

    def LD_F_Vx(self, opcode: Opcode) -> None:
        """
        $Fx29 - Set I = location of sprite for digit Vx.
        """
        self.I = (self.V[opcode.x] * 5) & 0x0FFF

    def LD_B_Vx(self, opcode: Opcode) -> None:
        """
        $Fx33 - Store BCD representation of Vx in memory locations I, I+1, and I+2.
        """
        self.memory.space[self.I] = self.V[opcode.x] // 100
        self.memory.space[self.I + 1] = (self.V[opcode.x] % 100) // 10
        self.memory.space[self.I + 2] = self.V[opcode.x] % 10

    def LD_I_Vx(self, opcode: Opcode) -> None:
        """
        $Fx55 - Store registers V0 through Vx in memory starting at location I.
        """
        for i in range(opcode.x + 1):
            self.memory.space[self.I + i] = self.V[i]

    def LD_Vx_I(self, opcode: Opcode) -> None:
        """
        $Fx65 - Read registers V0 through Vx from memory starting at location I.
        """
        for i in range(opcode.x + 1):
            self.V[i] = self.memory.space[self.I + i]

    @property
    def optable(self):
        return {
            0x0000: self.SYS_addr,
            0x1000: self.JP_addr,
            0x2000: self.CALL_addr,
            0x3000: self.SE_Vx_byte,
            0x4000: self.SNE_Vx_byte,
            0x5000: self.SE_Vx_Vy,
            0x6000: self.LD_Vx_byte,
            0x7000: self.ADD_Vx_byte,
            0x8000: self.JP_addr_8,
            0x9000: self.SNE_Vx_Vy,
            0xA000: self.LD_I_addr,
            0xB000: self.JP_V0_addr,
            0xC000: self.RND_Vx_byte,
            0xD000: self.DRW_Vx_Vy_nibble,
            0xE000: self.Jp_addr_E,
            0xF000: self.Jp_addr_F,
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
        self.PC += 2
        operation(opcode)


        if not self.halt:
            if self.DT > 0:
                self.DT -= 1

            if self.ST > 0:
                self.ST -= 1

    def _log_state(self, operation, opcode):
        table = tabulate(
            (
                ("Op", f"{operation.__name__}({hex(opcode.type)})"),
                ("DATA", hex(self.memory.space[self.PC])),
                ("PC", hex(self.PC)),
                ("I", hex(self.I)),
                ("V", self.V),
            ),
            headers=("Variable", "Value"),
            tablefmt="github",
        )
        logging.debug(f"\n{table}\n")
