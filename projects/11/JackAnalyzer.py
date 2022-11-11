# code for the JACK Compiler (Chapter 11)
# Written by Devashish Tupkary

# Tokenizer can be better written- but it works in its current form..



import sys 
import os



global SYMBOL_LIST
SYMBOL_LIST = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']

global KEYWORD_LIST
KEYWORD_LIST = ['class','constructor','function','method','field','static','var','int','char','boolean','void','true','false',
                'null','this','let','do','if','else','while','return']

global DELIMITIERS
DELIMITERS = [' ','\n']

class Tokenizer:

    def __init__(self, inputpath):
        self.filename = inputpath #sets the filename we must read
        self.file = self.load()
        self.current_token = ""
        self.stop_flag = False
        self.tokens = self.return_all_tokens() #all tokens are now in a list.
        self.index = 0
        self.max_index = len(self.tokens)

    def advance(self):
        self.index = self.index+1
        return self.tokens[self.index-1]
    

    def next_token(self):
        
        return self.tokens[self.index]

    def token_type(token):
        if token.startswith("\""):
            return "stringConstant"
        elif token.isnumeric():
            return "integerConstant"
        elif token in SYMBOL_LIST:
            return "symbol"
        elif token in KEYWORD_LIST:
            return "keyword"
        elif token != "": 
            return "identifier"
        

    def has_next_token(self):
        if self.index < self.max_index:
            return True
        else:
            return False

   
    def generate_next_token(self): 
        while(True):
            if (self.current_token.startswith("\"")): # we are parsing string constant
                self.current_token = self.current_token + self.next_element()
                if self.current_token.endswith("\""):
                    token = self.current_token
                    self.current_token = ""
                    return token
                else:
                    continue

            if (self.current_token in SYMBOL_LIST): # we already have a token
                token = self.current_token
                self.current_token = ""
                return token
        
            if (self.current_token in DELIMITERS):
                self.current_token = ""
                return self.generate_next_token()
        
            current_char = self.next_element()
            
            if (current_char in SYMBOL_LIST):
                
                if (self.current_token == ""): #empty token
                    token = current_char
                    self.current_token = ""
                    return token
                else:
                    token = self.current_token
                    self.current_token = current_char
                    return token

            elif (current_char in DELIMITERS):
                if (self.current_token == ""): #empty token
                    return self.generate_next_token()
                else:
                    token = self.current_token
                    self.current_token = ""
                    return token

            elif (current_char == None):# we have reached end of file
                self.stop_flag = True #stop iterating
                return self.current_token
        
            #if none of the above. then append.
        
            self.current_token = self.current_token + current_char

    

    def string_val(self):
        if self.current_token.startswith("\"") and self.current_token.endswith("\""):
            return self.current_token[3:-2]

    ## HELPER FUNCTIONS ####
    def load(self):
        file = open(self.filename,"r")
        data = file.read() #the data is now just a giant string
        data = data.split("\n") #separates the data into different lines.
        
        

        comment = False #are we parsing a multiline comment?

        for (index,line) in enumerate(data): 
            #Loop logic can fail if multiple types of comments are present in each line.
            

            if comment == False:
                if (line.find("//") > -1): #line contains a single line comment
                    data[index] = line[0:line.find("//")] # remove the last line comment.

                if (line.find("/*")> -1): # line contains start of comment
                    if (line.rfind("*/") == -1):   #line does not contain end of comment
                        comment = True
                    
                    data[index] = line[0:line.find("/*")]
                    
                    
                    ## i assume that there is nothing after */ in the line
                             
            
            if comment == True: # we are parsing a multiline comment
                if (line.rfind("*/") > -1): # line contains end of comment
                    data[index] = line[line.rfind("*/")+2:]
                    comment = False
                else:
                    data[index] = ""
        
        data = [line.strip() for line in data] #strip line of trailing spaces
        data = [line for line in data if line != ""] #removes lines which are empty
        data_stream = " ".join(data)



        return iter(data_stream) #construct iterable object. 


    def next_element(self): #checks if there is a next element, and adds it to the current_char
        return next(self.file,None)
    
    def return_all_tokens(self):
        list = []
        while(not self.stop_flag):
            token = self.generate_next_token()
            if token != '':
                list.append(token)
        return list


class CompilationEngine():
    def __init__(self,output_file):
        self.filename = output_file
        self.file = open(output_file,"w")
        self.indent = ""
    
    def increase_indent(self):
        self.indent = self.indent+"  "

    def decrease_indent(self):
        self.indent = self.indent[0:-2]

    def write(self,string):
        self.file.write(self.indent+string)

    def write_terminal(self,tokenizer): #writes the next token which should be terminal token
        
        token = tokenizer.advance()
        token_type = Tokenizer.token_type(token)

        if token == '<':
            token = "&lt;"
        elif token == '>':
            token = "&gt;"
        elif token == '&':
            token = "&amp;"

        if token_type == "stringConstant":
            token = token[1:-1]
        self.file.write(self.indent+"<"+token_type+"> "+token+" </"+token_type+">\n")
    

    def write_terminals_until(self,tokenizer,symbol): # keeps writing terminals and stops after writing symbol
        while (tokenizer.next_token() != symbol):
            self.write_terminal(tokenizer)
        self.write_terminal(tokenizer)

    
    def write_terminals_before(self,tokenizer,symbol): # keeps writing terminals and stops BEFORE writinig symbol
        while (tokenizer.next_token() != symbol):
            self.write_terminal(tokenizer)

    def CompileClass(self,tokenizer):
        self.write("<class>\n")
        self.increase_indent()

        self.write_terminals_until(tokenizer,'{')

        while tokenizer.next_token() in ['static','field']:
            self.CompileclassVarDec(tokenizer)

        while tokenizer.next_token() in ['function','constructor','method']:
            self.CompilesubroutineDec(tokenizer)


        self.write_terminal(tokenizer) # would be }

        self.decrease_indent()
        self.file.write("</class>\n")

    
    
    def CompileclassVarDec(self,tokenizer):
        self.write("<classVarDec>\n")
        self.increase_indent()

        self.write_terminals_until(tokenizer,";")
     

        self.decrease_indent()
        self.write("</classVarDec>\n")
        

    def CompilesubroutineDec(self,tokenizer):
        self.write("<subroutineDec>\n")
        self.increase_indent()

        self.write_terminals_until(tokenizer,"(")
     
    
        self.CompileParameterList(tokenizer)

        self.write_terminal(tokenizer) #will be )

        #code for subroutine body now

        self.write("<subroutineBody>\n")
        self.increase_indent()

        self.write_terminal(tokenizer) #should be {
        while (tokenizer.next_token() == 'var'):
            self.CompilevarDec(tokenizer)
        
        self.CompileStatements(tokenizer)

        self.write_terminal(tokenizer) # should be }

        self.decrease_indent()
        self.write("</subroutineBody>\n")

        self.decrease_indent()
        self.write("</subroutineDec>\n")


    def CompilevarDec(self,tokenizer):

        self.write("<varDec>\n")
        self.increase_indent()

        self.write_terminals_until(tokenizer,";")
       
        self.decrease_indent()
        self.write("</varDec>\n")
        

    def CompileParameterList(self,tokenizer):
        self.write("<parameterList>\n")
        self.increase_indent()

        self.write_terminals_before(tokenizer,")")

        
        self.decrease_indent()
        self.write("</parameterList>\n")


    def CompileStatements(self,tokenizer):

        
        self.write("<statements>\n")
        self.increase_indent()

        
        while (tokenizer.next_token() in ['let','if','while','do','return']): #there is another statement to write

            nexttoken = tokenizer.next_token()
            if nexttoken == 'let':
                self.CompileLet(tokenizer)
            elif nexttoken == 'if':
                self.CompileIf( tokenizer)
            elif nexttoken == 'while':
                self.CompileWhile( tokenizer)
            elif nexttoken == 'do':
                self.CompileDo(tokenizer)
            elif nexttoken == 'return':
                self.CompileReturn( tokenizer)

        self.decrease_indent()
        self.write("</statements>\n")


    def CompileLet(self, tokenizer):
        self.write("<letStatement>\n")
        self.increase_indent()

        self.write_terminal(tokenizer)# has to be "let"
        self.write_terminal(tokenizer) # has to be varname

        if tokenizer.next_token() == '[':
            self.write_terminal(tokenizer) # has to be [
            self.CompileExpression(tokenizer)
            self.write_terminal(tokenizer) # has to be ]


        self.write_terminal(tokenizer) # has to be =
        self.CompileExpression(tokenizer)
        self.write_terminal(tokenizer) # has to be ;


        self.decrease_indent()
        self.write("</letStatement>\n")

    def CompileIf(self, tokenizer):
        self.write("<ifStatement>\n")
        self.increase_indent()
        
        self.write_terminal(tokenizer) # has to be IF
        self.write_terminal(tokenizer) # has to be (
        self.CompileExpression(tokenizer) 
        self.write_terminal(tokenizer) # has to be )

        self.write_terminal(tokenizer) # has to be {
        self.CompileStatements(tokenizer)
        self.write_terminal(tokenizer) # has to be }

        if tokenizer.next_token() == 'else':
            self.write_terminal(tokenizer)# has to be 'else'
            self.write_terminal(tokenizer)# has to be {
            self.CompileStatements(tokenizer)
            self.write_terminal(tokenizer)# has to be }

        self.decrease_indent()
        self.write("</ifStatement>\n")

    def CompileWhile(self, tokenizer):
        self.write("<whileStatement>\n")
        self.increase_indent()

        self.write_terminal(tokenizer) # must be 'while'
        self.write_terminal(tokenizer)
        self.CompileExpression(tokenizer)
        self.write_terminal(tokenizer) # must be )

        self.write_terminal(tokenizer)
        self.CompileStatements(tokenizer)
        self.write_terminal(tokenizer) # must be )


        self.decrease_indent()
        self.write("</whileStatement>\n")



    def CompileDo(self, tokenizer):
        self.write("<doStatement>\n")
        self.increase_indent()

        self.write_terminal(tokenizer) # must be 'do'
        ## noe we must do subroutineCall

        self.write_terminal(tokenizer) #subroutine name / classnameorvarname

        if tokenizer.next_token() == '(':
            self.write_terminal(tokenizer) # (
            self.CompileExpressionList(tokenizer)
            self.write_terminal(tokenizer) # must be )

        elif tokenizer.next_token() == ".":
            self.write_terminals_until(tokenizer,"(") # 
            self.CompileExpressionList(tokenizer)
            self.write_terminal(tokenizer) # must be )

        self.write_terminal(tokenizer) # must  be ;
        self.decrease_indent()
        self.write("</doStatement>\n")
        
    
    def CompileReturn(self, tokenizer):
        self.write("<returnStatement>\n")
        self.increase_indent()

        self.write_terminal(tokenizer) # must be return

        if tokenizer.next_token() != ';': # there is a return expression
            self.CompileExpression(tokenizer)
        
        self.write_terminal(tokenizer) # must be ;


        self.decrease_indent()
        self.write("</returnStatement>\n")

    def CompileExpression(self, tokenizer):
        self.write("<expression>\n")
        self.increase_indent()

        self.CompileTerm(tokenizer)

       

        while tokenizer.next_token() in ['+','-','*','/','&','|','<','>','=']: #there is another term
            self.write_terminal(tokenizer) # will be the above symbol
            self.CompileTerm(tokenizer)


        self.decrease_indent()
        self.write("</expression>\n")

    def CompileExpressionList(self, tokenizer):
        self.write("<expressionList>\n")
        self.increase_indent()

        if tokenizer.next_token() != ')': # there is atleast one
            self.CompileExpression(tokenizer)
            while tokenizer.next_token() != ')':
                self.write_terminal(tokenizer) # must be ;
                self.CompileExpression(tokenizer)



        self.decrease_indent()
        self.write("</expressionList>\n")

    def CompileTerm(self, tokenizer):

        self.write("<term>\n")
        self.increase_indent()

        nexttoken = tokenizer.next_token()

        if nexttoken in ['-','~']: #unary op
            self.write_terminal(tokenizer) 
            self.CompileTerm(tokenizer)
        
        elif nexttoken == '(':

            self.write_terminal(tokenizer) # will be some 
            self.CompileExpression(tokenizer)
            self.write_terminal(tokenizer)
        
        else:
            self.write_terminal(tokenizer) # wil be something

            nexttoken = tokenizer.next_token()
            if nexttoken == '[': # array indexing
                self.write_terminal(tokenizer)
                self.CompileExpression(tokenizer)
                self.write_terminal(tokenizer)
            
            elif nexttoken == '(': 
                self.write_terminal(tokenizer)
                self.CompileExpressionList(tokenizer)
                self.write_terminal(tokenizer)

            elif nexttoken == '.':
                self.write_terminal(tokenizer)
                self.write_terminal(tokenizer)
                self.write_terminal(tokenizer)

                self.CompileExpressionList(tokenizer)
                self.write_terminal(tokenizer)
                
        self.decrease_indent()
        self.write("</term>\n")

        
       
class SymbolTable:

    def __init__(self):
        self.symbol_table = {}
        self.static_count = 0
        self.field_count = 0
        self.arg_count = 0
        self.var_count = 0

    def startSubroutine(self):
        self.subroutine_table = {}
        self.arg_count    = 0
        self.var_count    = 0



    def define(self,name,type,kind):
        
        if kind == "static":
            num = self.static_count
            self.static_count = self.static_count + 1
            self.symbol_table[name] = (type,kind,num)
        
        elif kind == 'field':
            num = self.field_count
            self.field_count = self.field_count+1
            self.symbol_table[name] = (type,kind,num)
        
        elif kind == "arg":
            num = self.arg_count
            self.arg_count = self.arg_count+1
            self.subroutine_table[name] = (type,kind,num)

        elif kind == "var":
            num = self.var_count
            self.var_count = self.var_count+1
            self.subroutine_table[name] = (type,kind,num)
        return

    def varcount(self,kind):
        if kind == 'field':
            return self.field_count
        elif kind == 'static':
            return self.static_count
        elif kind == 'var':
            return self.var_count
        elif kind == 'arg':
            return self.arg_count
        else:
            print("something is wrong\n")
            return 0

    def kindof(self,name):
        if name in self.subroutine_table.keys():
            value = self.subroutine_table[name]
            return value[1]
        elif name in  self.symbol_table.keys():
            value = self.symbol_table[name]
            return value[1]

    def typeof(self,name):
        if name in self.subroutine_table.keys():
            value = self.subroutine_table[name]
            return value[0]
        elif name in  self.symbol_table.keys():
            value = self.symbol_table[name]
            return value[0]
    
    def indexof(self,name):
        if name in self.subroutine_table.keys():
            value = self.subroutine_table[name]
            return value[2]
        elif name in  self.symbol_table.keys():
            value = self.symbol_table[name]
            return value[2]



class VM_Writer: #writes the VM commants
    def __init__(self,output_file):
        self.filename = output_file
        self.file = open(output_file,"w")
       
    def write(self,string):
        self.file.write(string)

    def write_list(self, list):#writes a list of words separated by white space
        for word in list:
            self.file.write(word+" ")
        self.file.write("\n")

    def writePush(self,segment,index):
        self.write_list(self,["push",segment,str(index)])

    def writePop(self,segment,index):
        self.write_list(self,["pop",segment,str(index)])

    def writeArithmetic(self,command):
        self.write(command+"\n")

    def writeLabel(self,string):
        self.write("label "+string+"\n")

    def writeGoto(self,string):
        self.write("goto {}\n".format(string))

    def writeIf(self, string):
        self.write("if-goto {}\n".format(string))

    def writeCall(self, string, nargs):
        self.write_list(self,["call",string,str(nargs)])
    
    def writeFunction(self, string, nlocals):
        self.write_list(self,["function",string,str(nlocals)])

    def writeReturn(self):
        self.write("return\n")

    def close(self):
        self.file.close()


        








input_path = sys.argv[1]
#input_path = "./Square/Square.jack"



if input_path.endswith(".jack"): #end of path is .vm, so file 
    output_file_path = input_path.replace(".jack",".xml")
    
    tokenizer = Tokenizer(input_path)
    writer = CompilationEngine(output_file_path)
    writer.CompileClass(tokenizer)

   
else : #its a directory
   
   
    for file_path in os.listdir(input_path):
        if file_path.endswith(".jack"):
            path = input_path +"/"+file_path
            tokenizer = Tokenizer(path)
            output_file_path = path.replace(".jack",".xml")
            print("Writing to "+output_file_path+"\n")
            writer = CompilationEngine(output_file_path)
            writer.CompileClass(tokenizer)

    
