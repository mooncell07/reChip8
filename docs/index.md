<h1 align="center">
<img src="./img/lemon.png" height=10>
<br>Lemon.pie
</h1>

Lemon is a **[CHIP-8](https://en.wikipedia.org/wiki/CHIP-8)** Emulator written in Python using Pygame.
This library aims at implementing the original and classic varient of CHIP-8 Virtual Machine. It is a toy just for my own learning experience and is in no way suitable for any
type of research for the original VM.

But, i have to say that it was really fun writing this emulator again after so many months!
My last implementation of the VM was "Trace-Fractal" that i archived, Lemon can be considered the successor of that project,
an attempt to make the codebase a tad bit more clean.


### Progress (So Far...):
So far, i have completed almost 90% of the emulator though there are a few things that are still
needed to be fixed:

- Clipping Quirk

- Disp.wait Quirk

- Keypad Not Halting Bug

Since i am going for classic CHIP-8 varient, i have to implement those quriks to match
original CHIP-8 behaviour.

### Test Results:

**Corax Test**:
![corax test](./img/test_opcode.png)

**Flags Test**:
![flags test](./img/flags-test.png)

**Quirks Test**:
![quirks test](./img/quirks-test.png)

**Halt Test**:
![halt test](./img/halt-test.png)

### Future Ahead:

I have decided to make an assembler and disassembler for this project as well and
eventually emulate other consoles like Gameboy and NES.
