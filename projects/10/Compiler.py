# code for the JACK to XML Compiler.


import sys 
import os

from attr import asdict

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
        self.file = self.load() #self.file is an iterator now. 
        self.current_token = ""
        self.stop_flag = False

   
    def next_token(self): 
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
                return self.next_token()
        
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
                    return self.next_token()
                else:
                    token = self.current_token
                    self.current_token = ""
                    return token

            elif (current_char == None):# we have reached end of file
                self.stop_flag = True #stop iterating
                return self.current_token
        
            #if none of the above. then append.
        
            self.current_token = self.current_token + current_char

    def token_type(self):
        if self.current_token.startswith("\""):
            return "STRING_CONST"
        elif self.current_token.isnumeric():
            return "INT_CONST"
        elif self.current_token in SYMBOL_LIST:
            return "SYMBOL"
        elif self.current_token in KEYWORD_LIST:
            return "KEYWORD"
        elif self.current_token != "": #sometimes we might get these empty tokens
            #typically towards the last token..
            return "INDENTIFIER"
        else:
            return "NONE"

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
                    data[index] = line[:line.rfind("*/")+2]
                    comment = True
                else:
                    data[index] = ""
        
        data = [line.strip() for line in data] #strip line of trailing spaces
        data = [line for line in data if line != ""] #removes lines which are empty
        data_stream = " ".join(data)

        return iter(data_stream) #construct iterable object. 


    def next_element(self): #checks if there is a next element, and adds it to the current_char
        return next(self.file,None)
        

    ### Checking functions, not used for compilation

    def print_all_tokens(self):
        while(not self.stop_flag):
            print(self.next_token())


class CompilationEngine():
    def __init__(self,output_file):
        self.filename = output_file
        self.file = open(output_file,"w")

    def write(self,string):
        self.file.write(string)

    
    def CompileClass(self, tokenizer):
        self.write{"<class>\n"}
        self.write("class")
        
        self.write("</class>\n")

    def CompileClassVarDec(self, tokenizer):

    def CompileSubroutine(self, tokenizer):

    def CompileParameterList(self, tokenizer):

    def CompileVarDec(self, tokenizer):

    def CompileStatements(self,tokenizer):

    def CompileDo(self,tokenizer):

    def CompileLet(self,tokenizer):

    def CompileWhile(self, tokenizer):
    
    def CompileReturn(self, tokenizer):

    def CompileIf(self, tokenizer):

    def CompileExpression(self, tokenizer):

    def CompileTerm(self, tokenizer):

    def CompileExpressionList(self, tokenizer):

    
