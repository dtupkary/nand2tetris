#VM_translator for Chapter 8 of the Nand2Tetris course.


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
        elif current_command[0] == "label" :
            return "C_LABEL"
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
        self.jump_index = 0
        self.call_index = 0
        self.current_parsing_file = ""
        self.function_name = "" # we can initialize this to zero, coz we need it to produce labels, and labels don't appear outside of functions :P

        #see https://www.coursera.org/learn/nand2tetris2/programming/p3jZ1/project-8/discussions/threads/jhdQ9ZxBEeifVAor9mp_ug
        return

    def set_parsing_file(self,parser_object):
        input_file_name = parser_object.filename.split("/")[-1]
        self.current_parsing_file = input_file_name.replace(".vm","")
        self.file.write("//{}\n".format(self.current_parsing_file)) # so we know when new file writing starts.


    def write(self,parser_object):
        command_type = parser_object.commandType()
        self.file.write("//{}\n".format(parser_object.current_inst)) #so we know what line is being written
        if command_type == "C_PUSH" or command_type == "C_POP":
            self.writePushPop(parser_object)
        if command_type =="C_ARITHMETIC":
            self.writeArithmetic(parser_object)

        if command_type == "C_GOTO":
            self.writeGoto(parser_object)
        if command_type == "C_IF":
            self.writeIf(parser_object)
        if command_type == "C_LABEL":
            self.writeLabel(parser_object)

        if command_type == "C_CALL":
            self.writeCall(parser_object)
        if command_type == "C_FUNCTION":
            self.writeFunction(parser_object)
        if command_type == "C_RETURN":
            self.writeReturn(parser_object)
        
        
    
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
            self.file.write("@JMPPOINT{}".format(str(self.jump_index))+"\n") #prep to jump
            
            if operation =="eq":
                self.file.write("D;JEQ\n") #Jump to label is true   
            if operation == "gt":
                self.file.write("D;JGT\n")
            if operation =="lt":
                self.file.write("D;JLT\n")
                #following assembly code sets M to false, and is only exected if statement is false
            self.set_A_to_stack()
            self.file.write("M=0\n") #M is false
            self.file.write("(JMPPOINT{}".format(str(self.jump_index))+")\n")
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
            
        else:
            raise Exception("Command type of parser and codewriter not matching")

    #Two functions in the same VM file can have identical label names, so you need to include the function name.
    #Because function names must be unique across all VM files in the program (so that they can be called), you do not need to include the VM File name.
    def writeGoto(self,parser_object):
        label = parser_object.arg1()
        self.file.write("@{}.{}\n".format(self.function_name,label))
        self.file.write("0;JMP\n")

    def writeLabel(self,parser_object):
        label = parser_object.arg1()
        self.file.write("({}.{})\n".format(self.function_name,label))
    
    def writeIf(self,parser_object):
        label = parser_object.arg1()
        self.pop_stack_to_D()
        self.file.write("@{}.{}\n".format(self.function_name,label))
        self.file.write("D;JNE\n")



    def writeFunction(self,parser_object):
        num_local = int(parser_object.arg2())
        self.function_name = parser_object.arg1()
        self.file.write("({})\n".format(self.function_name))
        for i in range(0,num_local):
            self.file.write("D=0\n") 
            self.push_D_to_stack()
        
    def writeCall(self, parser_object):
        #We end the assembly code for call with (returnAddress). Thus, after the call ends (Via return), the execution must 
        # proceed by starting execution form the label of return Address..

        # note because we might call a function multiple times, eeach time the return address must be unique ...

        function_name = parser_object.arg1()
        nargs = int(parser_object.arg2())

        ret_address = function_name + "RET"+str(self.call_index)
        self.call_index += 1

        #push return-address
        self.file.write("@{}\n".format(ret_address))
        self.file.write("D=A\n")
        self.push_D_to_stack()

        #push LCL, ARG, THIS, THAT

        for symbol in ["LCL","ARG","THIS","THAT"]:
            self.file.write("@{}\n".format(symbol))
            self.file.write("D=M\n")
            self.push_D_to_stack()
        
        #LCL = SP
        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@LCL\n")
        self.file.write("M=D\n")

        #ARG = SP - narg - 5
        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@{}\n".format(nargs+5))
        self.file.write("D=D-A\n")
        self.file.write("@ARG\n")
        self.file.write("M=D\n")
        
        #goto f.

        self.file.write("@{}\n".format(function_name))
        self.file.write("0;JMP\n")
         
        self.file.write('({})'.format(ret_address))

    def writeCall_functionnameinput(self, function_name, nargs):
        #We end the assembly code for call with (returnAddress). Thus, after the call ends (Via return), the execution must 
        # proceed by starting execution form the label of return Address..

        # note because we might call a function multiple times, eeach time the return address must be unique ...

        ret_address = function_name + "RET"+str(self.call_index)
        self.call_index += 1

        #push return-address
        self.file.write("@{}\n".format(ret_address))
        self.file.write("D=A\n")
        self.push_D_to_stack()

        #push LCL, ARG, THIS, THAT

        for symbol in ["LCL","ARG","THIS","THAT"]:
            self.file.write("@{}\n".format(symbol))
            self.file.write("D=M\n")
            self.push_D_to_stack()
        
        #LCL = SP
        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@LCL\n")
        self.file.write("M=D\n")

        #ARG = SP - narg - 5
        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@{}\n".format(nargs+5))
        self.file.write("D=D-A\n")
        self.file.write("@ARG\n")
        self.file.write("M=D\n")
        
        #goto f.

        self.file.write("@{}\n".format(function_name))
        self.file.write("0;JMP\n")

        self.file.write('({})'.format(ret_address))

    def writeReturn(self,parser_object):

        #R14 = frame
        #R15 = ret

        self.file.write("@LCL\n")
        self.file.write("D=M\n") 
        self.file.write("@R14\n")
        self.file.write("M=D\n") #saves LCL in R14

        self.file.write("@R14\n")
        self.file.write("D=M\n")
        self.file.write("@5\n")
        self.file.write("D=D-A\n") #D is now the address that stores return address value.
        self.file.write("A=D\n") # A is now the address that stores the return address value.
        self.file.write("D=M\n") # D is now the return address value. 
        self.file.write("@R15\n")
        self.file.write("M=D\n") #saves return address to R15

        # *ARG = pop()
        self.pop_stack_to_D()
        self.file.write('@ARG\n')
        self.file.write('A=M\n')
        self.file.write('M=D\n')

        # SP = ARG+1
        self.file.write('@ARG\n')
        self.file.write('D=M\n')
        self.file.write('@SP\n')
        self.file.write('M=D+1\n')

        # THAT = *(FRAME-1)
        # THIS = *(FRAME-2)
        # ARG = *(FRAME-3)
        # LCL = *(FRAME-4)
        offset = 1
        for address in ['@THAT', '@THIS', '@ARG', '@LCL']:
            self.file.write('@R14\n')
            self.file.write('D=M\n') # Save start of frame
            self.file.write('@{}\n'.format(str(offset)))
            self.file.write('D=D-A\n') # Adjust address
            self.file.write('A=D\n') # Prepare to load value at address
            self.file.write('D=M\n') # Store value
            self.file.write(address+"\n")
            self.file.write('M=D\n') # Save value
            offset += 1

        # goto RET
        self.file.write('@R15\n')
        self.file.write('A=M\n')
        self.file.write('0;JMP\n')

    def setup_init(self):
        self.file.write('@256\n')
        self.file.write('D=A\n')
        self.file.write('@SP\n')
        self.file.write('M=D\n') #stack pointer is set to 256 
        self.writeCall_functionnameinput('Sys.init', 0)
        # self.file.write('@Sys.init')
        # self.file.write('0;JMP')







    #Helper functions

    def decrement_SP(self):
        self.file.write('@SP\n')
        self.file.write('M=M-1\n')

    def increment_SP(self):
        self.file.write('@SP\n')
        self.file.write('M=M+1\n')

    def set_A_to_stack(self):
        self.file.write('@SP\n')
        self.file.write('A=M\n')

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

        if segment == "static":
            # we need first the filename and thenwe can index as file.segment
            name = self.current_parsing_file+"."+index
            self.file.write("@"+name+"\n")


    def push_D_to_stack(self):
        self.file.write("@SP\n") #A stores the location of the location of SP
        self.file.write("A=M\n") #A stores location of SP
        self.file.write("M=D\n") # add value to stack
        self.file.write("@SP\n") 
        self.file.write("M=M+1\n") #increment stack
        
    def pop_stack_to_D(self):
        self.file.write("@SP\n") # A stores location of locationn of SP
        self.file.write("M=M-1\n") #decrement stack.
        self.file.write("A=M\n") # A stores location of SP
        self.file.write("D=M\n") #D stores top of stack
        


    
        





def main(parser,cw): #simple function that takes a parser, codewriter and starts translating
    while parser.current_inst != "": #while parser has not reached end of while
        if parser.is_instruction():
            cw.write(parser) 
        parser.read_next_instruction()

    print("*** Translation completed ***")





#input_path = sys.argv[0]
#print("Input path is ",input," \n. Starting Translation \n ")
input_path = sys.argv[1]


if input_path.endswith(".vm"): #end of path is .vm, so file
    output_file_path = input_path.replace(".vm",".asm")
    
    parser= Parser(input_path)
    cw = CodeWriter(output_file_path)
    #cw.setup_init()
    cw.set_parsing_file(parser)
    main(parser,cw)

   
else : #its a directory
    output_file_path = input_path+"/"+input_path.split("/")[-1]+".asm"

    cw = CodeWriter(output_file_path)
    cw.setup_init()

    for file_path in os.listdir(input_path):
        if file_path.endswith(".vm"):
            parser = Parser(input_path +"/"+file_path)
            cw.set_parsing_file(parser) #so that codewriter knows which file it is parsing
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





    

    
