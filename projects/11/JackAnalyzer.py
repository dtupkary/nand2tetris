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


global CONVERT_KIND
CONVERT_KIND = {     'arg': 'arg',    'static': 'static',    'var': 'local',    'field': 'this'  }

global ARITHMETIC 
ARITHMETIC = {    '+': 'add',    '-': 'sub',    '=': 'eq',    '>': 'gt',    '<': 'lt',    '&': 'and',    '|': 'or'  }

global ARITHMETIC_UNARY
ARITHMETIC_UNARY = {    '-': 'neg',    '~': 'not'  }

global while_index 
while_index = 0

global if_index
if_index = 0

  

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
        #self.writer = VM_Writer(output_file) 
        self.symbol_table = SymbolTable()   
        self.classname = ""
        

    def CompileClass(self,tokenizer,writer):
        token = tokenizer.advance()  #class
        self.classname = tokenizer.advance() #className
        tokenizer.advance() #{

        while tokenizer.next_token() in ['static','field']:
            self.CompileclassVarDec(tokenizer, writer)

        while tokenizer.next_token() in ['function','constructor','method']:
            self.CompilesubroutineDec(tokenizer, writer)


        self.writer.close()
    
    
    def CompileclassVarDec(self,tokenizer, writer):
        kind = tokenizer.advance() #(static | field)
        type = tokenizer.advance() #(type)
        name = tokenizer.advance() #name

        self.symbol_table.define(name,type,kind)

        while (tokenizer.next_token() != ';'):
            tokenizer.advance() # ","
            name = tokenizer.advance() # name
            self.symbol_table.define(name,type,kind)

        tokenizer.advance() # will be ;


        
        

    def CompilesubroutineDec(self,tokenizer, writer):
        
        subroutine_kind = tokenizer.advance() # constructor / method  / function
        return_type = tokenizer.advance() # return type
        subroutine_name = tokenizer.advance() # 

        self.symbol_table.startSubroutine()

        if subroutine_kind == 'method':
            self.symbol_table.define('instance',self.classname,'arg')

        tokenizer.advance() # '('
        self.CompileParameterList(self, tokenizer, writer) 

        tokenizer.advance() # must be )
        tokenizer.adance() # must be  {

        while tokenizer.next_token() == 'var':
            self.compileVarDec(tokenizer,writer)

        function_name = '{}.{}'.format(self.class_name, subroutine_name)
        num_locals = self.symbol_table.varCount('var')
        writer.writeFunction(function_name, num_locals)

        if subroutine_kind == 'constructor':
            num_fields = self.symbol_table.varCount('FIELD')
            writer.writePush('constant', num_fields) #pushes number of fields
            writer.writeCall('Memory.alloc', 1) # calls Memory.alloc with one argument (which is the topmost stack point)
            writer.writePop('pointer', 0)
        elif subroutine_kind == 'method':
            self.vm_writer.writePush('arg', 0)
            self.vm_writer.writePop('pointer', 0)

        self.compileStatements(tokenizer, writer) # statements
        tokenizer.advance()# '}'


    def CompilevarDec(self,tokenizer, writer):

        tokenizer.advance()# 'var'
        type = tokenizer.advance()() # type
        name = tokenizer.advance()() 

        self.symbol_table.define(name, type, 'var')

        while tokenizer.next_token() != ';': # there is one more varname
            tokenizer.advance() # ','
            name = tokenizer.advance() # varName
            self.symbol_table.define(name, type, 'var')

        tokenizer.advance() # ';'

  
    def CompileParameterList(self,tokenizer, writer): #yes I konw this doesnt write anything, but its easier to pass tokenizer and writer to everything 
        if tokenizer.next_token() != ')': #there is atleast one argument
            type = tokenizer.advance() # type
            name = tokenizer.advance() # varName

            self.symbol_table.define(name, type, 'arg')

        while tokenizer.next_token() != ')' : # there is more arguments 
            tokenizer.advancec() # must be ,
            type = tokenizer.advance()
            name = tokenizer.advance()
            self.symbol_table.define(name, type, 'arg')


    def CompileStatements(self,tokenizer, writer):

        
        while (tokenizer.next_token() in ['let','if','while','do','return']): #there is another statement to write

            nexttoken = tokenizer.next_token()
            if nexttoken == 'let':
                self.CompileLet(tokenizer, writer)
            elif nexttoken == 'if':
                self.CompileIf( tokenizer, writer)
            elif nexttoken == 'while':
                self.CompileWhile( tokenizer, writer)
            elif nexttoken == 'do':
                self.CompileDo(tokenizer, writer)
            elif nexttoken == 'return':
                self.CompileReturn( tokenizer, writer)


    def CompileDo(self, tokenizer, writer):
        
        tokenizer.advance() # must be 'do'
        ## noe we must do subroutineCall

        self.CompileSubroutineCall(self, tokenizer, writer)

       
        writer.writePop('temp', 0) #Why is this needed ??
        tokenizer.advance() # ;

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def CompileLet(self, tokenizer, writer):
        tokenizer.advance() # must be let

        varname = tokenizer.advance() 
        varkind = CONVERT_KIND[self.symbol_table.kindOf(varname)]
        varindex = self.symbol_table.indexOf(varname)

        if tokenizer.next_token() == '[':
            tokenizer.advance() # has to be [
            self.CompileExpression(tokenizer, writer) # the value of the index of the array has been pushed onto stack
            tokenizer.advance(tokenizer) # has to be ] 

            writer.writePush(varkind, varindex)
            writer.writeArithmetic('add')
            writer.writePop('temp',0) # store this address in temp.

            tokenizer.advance() # must be =
            tokenizer.compileExpression() #
            tokenizer.advance() # ;

            writer.writePush('temp',0)
            writer.writePop('pointer',1) # pop the array location to pointer 1. therefore that  is set to the location of the place in the array.
            writer.writePop('that',0) # pop the RHS of = to that .., which is the array location....

        else : #regular assignment
            tokenizer.advance() # has to be =
            self.CompileExpression(tokenizer)
            tokenizer.advance() # has to be ;

            writer.writePop(varkind,varindex) # pop the value and store it in var

## 'if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
    def CompileIf(self, tokenizer, writer):
        
        tokenizer.advance() # must be if
        tokenizer.advance() # must be (
        
        self.CompileExpression(tokenizer,writer)
        writer.writeArirthmetic('not')

        writer.writeIf("if_false{}".format(if_index)) # jumps if ifcondition is false.

        tokenizer.advance() # )
        tokenizer.advance() # {
        
        self.CompileStatements(tokenizer,writer)

        tokenizer.advance() #}
        writer.writeGoto("if_true{}".format(if_index)) # always jumps if condition is true..
        writer.writeLabel("if_false{}".format(if_index))
        
        
        if tokenizer.next_token() == 'else': # there exists an else statement
            tokenizer.advance() # else

            tokenizer.advance() #{
            self.compileStatements(tokenizer, writer)
            tokenizer.advance() #}

        writer.Label("if_true{}".format(if_index)) # 
       
        if_index = if_index + 1
  
    # 'while' '(' expression ')' '{' statements '}'
    def CompileWhile(self, tokenizer, writer):
        tokenizer.advance() # must be while
        tokenizer.advance() # must be (
            
        writer.writeLabel('while{}\n'.format(while_index))
        
        self.compileExpression(tokenizer,writer)
        writer.writeArithmetic('not') # evaluatate false doncition.

        tokenizer.advance() # is )
        tokenizer.advance() # is {

        writer.writeIf('while_end{}\n"'.format(while_index)) #if true, got to end of while loop
        self.compileStatements(tokenizer,writer)
        tokenizer.advance() # must be }

        writer.writeGoto('while{}\n'.format(while_index))
        writer.writeLabel('while_end{}\n'.format(while_index))

    
    # 'return' expression? ';'
    def CompileReturn(self, tokenizer, writer):
       
        tokenizer.advance() # must be return

        if tokenizer.next_token() != ';': # there is a return expression
            self.CompileExpression(tokenizer)
        else: # push dummy
            writer.writePush('constant',0)

        writer.writeReturn()
        tokenizer.advance()


###### start to write here. 

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



    ### HELPER FUNCTIONS
    # subroutineCall: subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
    def compile_subroutine_call(self, tokenizer, writer):
        identifier = tokenizer.advance() # (subroutineName | className | varName)
        function_name = identifier
        number_args = 0

        if tokenizer.next_token()  == '.':
            tokenizer.advance()
            subroutine_name = tokenizer.advance()  # subroutineName

            type = self.symbol_table.typeOf(identifier)

            if type != 'none': # it's an instance, and not a class!
                instance_kind = self.symbol_table.kindOf(identifier)
                instance_index = self.symbol_table.indexOf(identifier)

                writer.writePush(CONVERT_KIND[instance_kind], instance_index)

                function_name = '{}.{}'.format(type, subroutine_name) 
                number_args += 1
            else: # it's a class
                class_name = identifier
                function_name = '{}.{}'.format(class_name, subroutine_name)
        
        elif tokenizer.next_token() == '(':
            subroutine_name = identifier
            function_name = '{}.{}'.format(self.class_name, subroutine_name)
            number_args = number_args + 1

            writer.writePush('pointer', 0)

        tokenizer.advance()             # '('
        number_args = number_args + self.compileExpressionList()  # expressionList. THis code must push correctly to stack, and return number of things pushed...
        tokenizer.advance()              # ')'

        writer.writeCall(function_name, number_args)

    

        
       
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
        return 'none'

    def typeof(self,name):
        if name in self.subroutine_table.keys():
            value = self.subroutine_table[name]
            return value[0]
        elif name in  self.symbol_table.keys():
            value = self.symbol_table[name]
            return value[0]
        return 'none'
    
    def indexof(self,name):
        if name in self.subroutine_table.keys():
            value = self.subroutine_table[name]
            return value[2]
        elif name in  self.symbol_table.keys():
            value = self.symbol_table[name]
            return value[2]
        return 'none'


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
    compiler = CompilationEngine(output_file_path)
    compiler.CompileClass(tokenizer)

   
else : #its a directory
   
   
    for file_path in os.listdir(input_path):
        if file_path.endswith(".jack"):
            path = input_path +"/"+file_path
            tokenizer = Tokenizer(path)
            output_file_path = path.replace(".jack",".xml")
            print("Writing to "+output_file_path+"\n")
            compiler = CompilationEngine(output_file_path)
            compiler.CompileClass(tokenizer)

    
