import sys

class BrainfuckMachine():
    class HeadOverflow(Exception):
        pass

    class BracketMismatch(Exception):
        pass

    def __init__(self, size) -> None:
        super().__init__()
        self.tape = [0] * size
        self.head = 0
        self.code = ''

    def check_brackets_mismatch(self) -> None:
        if (self.code.count('[') != self.code.count(']')):
            raise self.BracketMismatch()

    def build_brackets_map(self) -> dict:
        temp_brackets_stack, brackets_map = [], {}

        for position, command in enumerate(self.code):
            if command == '[':
                temp_brackets_stack.append(position)
            if command == ']':
                start = temp_brackets_stack.pop()
                brackets_map[start] = position
                brackets_map[position] = start

        return brackets_map

    def run(self) -> None:
        self.check_brackets_mismatch()
        code_ptr = 0
        brackets_map = self.build_brackets_map()

        while code_ptr < len(self.code):
            command = self.code[code_ptr]

            if command == '>':
                self.head += 1
                if (self.head >= len(self.tape)):
                    raise self.HeadOverflow()

            if command == '<':
                self.head -= 1
                if (self.head < 0):
                    raise self.HeadOverflow()

            if command == '+':
                if self.tape[self.head] == 255:
                    self.tape[self.head] = 0
                else:
                    self.tape[self.head] += 1

            if command == '-':
                if self.tape[self.head] == 0:
                    self.tape[self.head] = 255
                else:
                    self.tape[self.head] -= 1

            if command == '[' and self.tape[self.head] == 0:              
                code_ptr = brackets_map[code_ptr]

            if command == ']' and self.tape[self.head] != 0:
                code_ptr = brackets_map[code_ptr]

            if command == '.':
                sys.stdout.write(chr(self.tape[self.head]))
            
            code_ptr += 1

