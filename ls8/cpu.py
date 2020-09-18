"""CPU functionality."""
loop_nums = []
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registry = [0] * 8
        self.pc = 0
        self.running = True
        self.Eflag = None
        # self.Lflag = None
        # self.Gflag = None


    def load(self):
        """Load a program into memory."""

        address = 0

        with open('examples/sctest.ls8') as f:
            for line in f:
                # replacing the hashmarks with nothing
                line = line.replace('#', '')
                # splitting the lines into lists and checking if they are the values needed
                # for isntructions and adding them to the ram if they are
                n = line.split()
                if len(n) > 0:
                    if 'TEST' in n[0]:
                        continue
                    if '1' in n[0] or '0' in n[0]:
                        self.ram[address] = int(n[0], 2)
                        address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registry[reg_a] += self.registry[reg_b]
        #elif op == "SUB": etc

        if op == 'MUL':
            self.registry[reg_a] *= self.registry[reg_b]
        else:
            raise Exception("Unsupported ALU operation")


    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # The list of instructions
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
        

        # Big gross If block
        while self.running:
            # getting the current instruction and the follow 2 values if they are needed
            instruction = self.ram[self.pc]
            oper_a = self.ram_read(self.pc+1)
            oper_b = self.ram_read(self.pc+2)

            if instruction == HLT:
                self.running = False
            if instruction == LDI:
                self.registry[oper_a] = oper_b
                self.pc += 3
            if instruction == PRN:
                print(self.registry[oper_a])
                self.pc += 2
            if instruction == MUL:
                # Sets the value of the oper_a index in the registry to
                # equal the product of both index values
                prod = self.registry[oper_a] * self.registry[oper_b]
                self.registry[oper_a] = prod
                self.pc += 3
            if instruction == CMP:
                # Compares the values at each given index and sets the equal flag
                # to true or false
                self.Eflag = self.registry[oper_a] == self.registry[oper_b]
                self.pc += 3
                # self.Gflag = self.registry[oper_a] > self.registry[oper_b]
                # self.Lflag = self.registry[oper_a] < self.registry[oper_b]
                    
            if instruction == JMP:
                # sets the counter to the value stored at the oper_a index in the registry
                self.pc = self.registry[oper_a]
            if instruction == JEQ:
                # If the equal flag is true, set pc to the value at oper_a index in the registry
                if self.Eflag == True:
                    self.pc = self.registry[oper_a]
                if self.Eflag == False:
                # otherwise we increment by 2
                    self.pc += 2
            if instruction == JNE:
                # if the eflag is false, set pc to be the value at oper_a index in registry
                if self.Eflag == False:
                    self.pc = self.registry[oper_a]
                # otherwise just increment by 2
                if self.Eflag == True:
                    self.pc += 2
            




    def ram_read(self, location):
        if location <= 255:
            return self.ram[location]

    def ram_write(self, location, value):
        if location <= 255:
            self.ram[location] = value
            return f'{value} placed at index {location}'

        return f'Sorry invalid location for {value}'
