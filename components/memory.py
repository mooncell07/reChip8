__all__ = ("Memory",)


class Memory:
    def __init__(self) -> None:
        self.space = bytearray(4096)

    def load_binary(self, binary, offset=0):
        with open(binary, "rb") as f:
            for i, data in enumerate(f.read()):
                self.space[i + offset] = data
