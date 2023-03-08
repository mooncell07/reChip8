import typing as t

__all__ = ("Opcode",)


class Opcode:
    """
    Operation code consisting of the information of a certain operation.
    """

    __slots__ = ("inst",)

    def __new__(cls, inst: int) -> t.Self:
        if isinstance(inst, int) and len(str(inst)) < 6:
            self = super(Opcode, cls).__new__(cls)
            return self

        else:
            raise ValueError(f"BAD OPCODE: {inst}")

    def __init__(self, inst: int) -> None:
        """
        Opcode Constructor.

        args:
            inst: instruction in the format of `hex(type|x|y|n|nn|nnn)`
        """
        self.inst = inst

    @property
    def type(self) -> int:
        """
        (first nibble) the type of operation.
        """
        value = self.inst & 0xF000
        return value

    @property
    def x(self) -> int:
        """
        (second nibble) general purpose register lookup.
        """
        value = (self.inst & 0x0F00) >> 8
        return value

    @property
    def y(self) -> int:
        """
        (third nibble) general purpose register lookup.
        """
        value = (self.inst & 0x00F0) >> 4
        return value

    @property
    def n(self) -> int:
        """
        (fourth nibble) 4-bit numeric value.
        """
        value = self.inst & 0x000F
        return value

    @property
    def kk(self) -> int:
        """
        (third and fourth nibble) 8-bit immediate.
        """
        value = self.inst & 0x00FF
        return value

    @property
    def nnn(self) -> int:
        """
        (second, third and fourth nibble) 12-bit immediate memory address.
        """
        value = self.inst & 0x0FFF
        return value

    def __repr__(self) -> str:
        return f"Opcode(inst={hex(self.inst)})"
