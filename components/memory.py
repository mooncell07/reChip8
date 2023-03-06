__all__ = ("Memory",)


class Memory:
    __slots__ = ("space",)

    def __init__(self) -> None:
        self.space: bytearray = bytearray(4096)

    def load_binary(self, binary: str, offset: int = 0) -> None:
        with open(binary, "rb") as f:
            for i, data in enumerate(f.read()):
                self.space[i + offset] = data
