#VM_translator for Chapter 7 of the Nand2Tetris course.

import os
from signal import raise_signal



global ARTHIMETIC_LIST
ARITHMETIC_LIST = ["add","sub","neg","eq","gt","lt","and","or","not"]

global location_dist
location_dict = {"SP":"R0", "local": "R1", "argument":"R2", "this":"R3", "that":"R4","temp":"R5", "static":"R16"}



#Class that parses through a given file
class Parser:

    
    def __init__(self, filename):
        self.filename = filename # set the file that we must read.
        self.file = open(self.filename, 'r') #open the file
        self.current_inst = self.file.readline() #read the first line.

    def read_next_instruction(self):
        self.current_inst=self.file.readline() #read next line
    
    def is_instruction(self): #check if current line is instruction or not. 
        self.current_inst=self.current_inst.strip()
        if len(self.current_inst)==0 or self.current_inst.startswith("//"):
            return False
        else:
            return True
    
    def commandType(self): #returnns command type of current command
        current_command = self.current_inst.split()
        if current_command[0] in ARITHMETIC_LIST : 
            return "C_ARITHMETIC"
        elif current_command[0] ==  "push" :
            return "C_PUSH"
        elif current_command[0] == "pop" :
            return "C_POP"
        elif current_command[0] == "goto" :
            return "C_GOTO"
        elif current_command[0] == "if-goto" :
            return "C_IF"
        elif current_command[0] == "function" :
            return "C_FUNCTION"
        elif current_command[0] == "return" :
            return "C_RETURN"
        elif current_command[0] == "call" :
            return "C_CALL"
        else:
            return("Command invalid")
    
    def arg1(self):
        current_command = self.current_inst.split()
        if self.commandType == "C_ARITHMETIC":
            return current_command[0]
        elif self.commandType == "C_RETURN":
            print("WARNING : Cannot call arg1 on RETURNN commands")
        return current_command[1]
    
    def arg2(self):
        current_command = self.current_inst.split()
        return current_command[2]


class trivial_CodeWriter:
    def __init__(self, filename):
        self.filename = filename # set the file that we must write into
        self.file = open(self.filename, 'w') #open the file
        return
    
    def write(self, line):
        self.file.write(line+"\n")
        return


class CodeWriter:
    def __init__(self, filename):
        self.filename = filename # set the file we must write into
        self.file = open(self.filename, 'w') #open the file
        return

    def writeArithmetic(parser_object):
        #write
        return



    def write(self,parser_object):
        command_type = parser_object.commandType()

        if command_type == "C_PUSH" or command_type == "C_POP":
            self.writePushPop(parser_object)
    

    def writePushPop(self,parser_object):
        #write 
        command_type = parser_object.commandType()

    
           
        
        arg1 = parser_object.arg1() #segment
        arg2 = parser_object.arg2() #index

        self.resolve_address(arg1,arg2) # A stores the location of object to be pushed / popped.

        if command_type == "C_PUSH":
            self.file.write("D=M\n") # D stores value to be pushed
            self.push_D_to_stack()
        elif command_type == "C_POP":
            self.pop_stack_to_D() # D stores value to be popped
            self.file.write("M=D\n") #store it in D

        else:
            raise Exception("Command type of parser and codewriter not matching")

        

       



    ### Helper functions

    def resolve_address(self,segment,index): #set the value of A to be the location of object to be pushed / popped

        if segment=="constant":
            self.file.write("@"+index+"\n") #A stores the constant value
            self.file.write("D=A\n") # D stores constant value
            self.file.write("@R13\n") # A stores R13
            self.file.write("M=D\n") # Location R13 stores D
            
        if segment in ["local","argument","this","that"]:
            self.file.write("@"+location_dict[segment]+"\n") # A stores location of location of base of segment.
            self.file.write("D=M\n")# D Stores location of based of segment
            self.file.write("@"+index+"\n")# A stores index
            self.file.write("A=D+A\n")# A stores location of segment[index].
            

        if segment == "pointer":
            self.file.write("@R3\n") #A stores location of base of segment
            self.file.write("D=A\n") # D Stores location of based of segment
            self.file.write("@"+index+"\n") # A stores indeex
            self.file.write("A=D+A\n") # A stores location of segment[index]/
            
        if segment == "temp":
            self.file.write("@R5\n") #A stores location of base of segment
            self.file.write("D=A\n") # D Stores location of based of segment
            self.file.write("@"+index+"\n") # A stores indeex
            self.file.write("A=D+A\n") # A stores location of segment[index]/
           


        ##to do add static.
    def push_D_to_stack(self):
        self.file.write("@SP\n") #A stores the location of the location of SP
        self.file.write("A=M\n") #A stores location of SP
        self.file.write("M=D\n") # add value to stack
        self.file.write("@SP\n") 
        self.file.write("M=M+1\n") #increment stack
    
    def pop_stack_to_D(self):
        self.file.write("@SP\n") # A stores location of locationn of SP
        self.file.write("A=M\n") # A stores location of SP
        self.file.write("D=M") #D stores top of stack
        self.file.write("@SP\n") #SP stores 
        self.file.write("M=M-1\n") #decrement stack.
    
        











input_path = "./testing/BasicTest.vm"
output_file_path = "./testing/Output.txt"


parser= Parser(input_path)
cw = CodeWriter(output_file_path)

while parser.current_inst != "": #while parser has not reached end of while
    if parser.is_instruction():
        cw.write(parser) 
    parser.read_next_instruction()

print("done")




## trivial codewriter check

"""
parser= Parser(input_path)
cw = trivial_CodeWriter(output_file_path)

while parser.current_inst != "": #while parser has not reached end of while
    if parser.is_instruction():
        cw.write(parser.current_inst + "||"+parser.commandType() ) 
    parser.read_next_instruction()

print("done")
"""





    

    
