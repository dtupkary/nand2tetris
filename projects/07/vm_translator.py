#VM_translator for Chapter 7 of the Nand2Tetris course.


import sys
import os


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
        if self.commandType() == "C_ARITHMETIC":
            return current_command[0]
        elif self.commandType() == "C_RETURN":
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

    """
     Contract between methods:
    1. Contents of the A and D registries are not guaranteed,
        so methods must set them to the values they need.
    2. Methods must always leave @SP pointing to the correct location.
    """

    def __init__(self, filename):
        self.filename = filename # set the file we must write into
        self.file = open(self.filename, 'w') #open the file
        self.jump_index=0
        return

    
    def write(self,parser_object):
        command_type = parser_object.commandType()

        if command_type == "C_PUSH" or command_type == "C_POP":
            self.writePushPop(parser_object)
        if command_type =="C_ARITHMETIC":
            self.writeArithmetic(parser_object)

    def writeArithmetic(self,parser_object):
        #write
        operation = parser_object.arg1() 
       
        if operation not in ['neg', 'not']: # Binary operator (comments refer to binary operations)
            self.pop_stack_to_D() #D stores y.
        self.decrement_SP()
        self.set_A_to_stack() # M = x


        if operation == "add":
            self.file.write("M=M+D\n")
        elif operation == "sub":
            self.file.write("M=M-D\n")
        elif operation == "and":
            self.file.write("M=D&M\n")
        elif operation == "or":
            self.file.write("M=D|M\n")
        elif operation == "neg":
            self.file.write("M=-M\n")
        elif operation == "not":
            self.file.write("M=!M\n")
        

        elif operation in ["eq", "gt", "lt"]:

            self.file.write("D=M-D\n") 
            self.file.write("M=-1\n") #put M as true tentatively.
            self.file.write("@jmppoint"+str(self.jump_index)+"\n") #prep to jump
            
            if operation =="eq":
                self.file.write("D:JEQ\n") #Jump to label is true   
            if operation == "gt":
                self.file.write("D:JGT")
            if operation =="lt":
                self.file.write("D:JLT")
                #following assembly code sets M to false, and is only exected if statement is false
            self.set_A_to_stack()
            self.file.write("M=0\n") #M is false
            self.file.write("(jmppoint"+str(self.jump_index)+"\n)")
            self.jump_index=self.jump_index+1



        self.increment_SP()


        
        return


    def writePushPop(self,parser_object):
        #write 
        command_type = parser_object.commandType()
       
        arg1 = parser_object.arg1() #segment
        arg2 = parser_object.arg2() #index
        
        if command_type == "C_PUSH":
            self.resolve_address(arg1,arg2) # A stores the location of object to be pushed / popped.
            if arg1 == "constant":
                self.file.write("D=A\n") #D stores value to be pushed
            else:
                self.file.write("D=M\n") # D stores value to be pushed
            self.push_D_to_stack()
            self.file.write("// completed a push \n")
        elif command_type == "C_POP":
            self.resolve_address(arg1,arg2) # A stores the location of object to be pushed / popped.
            self.file.write("D=A\n")
            self.file.write("@R13\n")
            self.file.write("M=D\n") #R13 stores location of object to be ppushed / popped.
            self.pop_stack_to_D() # D stores value to be popped
            #but now A might be changed, we need A to be the content of R13
            self.file.write("@R13\n")
            self.file.write("A=M\n")
            self.file.write("M=D\n") #pop it to 
            self.file.write("// completed a pop \n")
        else:
            raise Exception("Command type of parser and codewriter not matching")

        

    def decrement_SP(self):
        self.file.write('@SP\n')
        self.file.write('M=M-1\n')

    def increment_SP(self):
        self.file.write('@SP\n')
        self.file.write('M=M+1\n')

    def set_A_to_stack(self):
        self.file.write('@SP\n')
        self.file.write('A=M\n')



    ### Helper functions

    def resolve_address(self,segment,index): #set the value of A to be the location of object to be pushed / popped

        if segment=="constant":
            self.file.write("@"+index+"\n") #A stores the constant value (NOT THE ADDRESS!!)
        
            
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




        
    def push_D_to_stack(self):
        self.file.write("@SP\n") #A stores the location of the location of SP
        self.file.write("A=M\n") #A stores location of SP
        self.file.write("M=D\n") # add value to stack
        self.file.write("@SP\n") 
        self.file.write("M=M+1\n") #increment stack
        self.file.write("// pushed D to stack \n")
    
    def pop_stack_to_D(self):
        self.file.write("@SP\n") # A stores location of locationn of SP
        self.file.write("M=M-1\n") #decrement stack.
        self.file.write("A=M\n") # A stores location of SP
        self.file.write("D=M\n") #D stores top of stack
        self.file.write("// popped stack to D \n")
        





def main(parser,cw): #simple function that takes a parser, codewriter and starts translating
    while parser.current_inst != "": #while parser has not reached end of while
        if parser.is_instruction():
            cw.write(parser) 
        parser.read_next_instruction()

    print("*** Translation completed ***")





#input_path = sys.argv[0]
#print("Input path is ",input," \n. Starting Translation \n ")


input_path = "./MemoryAccess/BasicTest"

if input_path.endswith(".vm"): #end of path is .vm, so file
    output_file_path = input_path.replace(".vm",".asm")
    
    parser= Parser(input_path)
    cw = CodeWriter(output_file_path)

    main(parser,cw)

   
else : #its a directory
    output_file_path = input_path+".asm"

    cw = CodeWriter(output_file_path)

    for file_path in os.listdir(input_path):
        if file_path.endswith(".vm"):
            parser = Parser(input_path +"/"+file_path)
            main(parser,cw)
    





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





    

    
