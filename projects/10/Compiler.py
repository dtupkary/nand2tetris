# code for the JACK to XML Compiler.

# Tokenizer can be better written. 

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
        self.file = self.load()
        self.current_token = ""
        self.stop_flag = False
        self.tokens = self.return_all_tokens() #all tokens are now in a list.
        self.index = 0
        self.max_index = len(self.tokens)

    def advance(self):
        self.index = self.index+1
        return self.tokens[self.index-1]
    

    def current_token(self):
        return self.tokens[self.index]

    def token_type(token):
        if token.startswith("\""):
            return "STRING_CONST"
        elif token.isnumeric():
            return "INT_CONST"
        elif token in SYMBOL_LIST:
            return "SYMBOL"
        elif token in KEYWORD_LIST:
            return "KEYWORD"
        elif token != "": #sometimes we might get these empty tokens
            #typically towards the last token..
            return "INDENTIFIER"
        else:
            return "NONE"
   
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

    def print_all_tokens(self):
        while(not self.stop_flag):
            print(self.next_token())
    
    def return_all_tokens(self):
        list = []
        while(not self.stop_flag):
            list.append(self.next_token())
        return list


class CompilationEngine():
    def __init__(self,output_file):
        self.filename = output_file
        self.file = open(output_file,"w")
       
        self.index = 0
    
    def write(self,string):
        self.file.write(string)

    
    def CompileClass(self , tokenizer):
        token = tokenizer.advance()
        self.write("<class>\n")
        self.write_terminal("keyword",token) #token should be ""class"
        class_name = tokenizer.advance() #should be classname
        self.write_terminal("identifier",class_name)
        symbol = tokenizer.advance() # should be {
        self.write("symbol",symbol)
        
        self.CompileClassVarDec(self, tokenizer)
        self.CompileSubroutine(self, tokenizer)
        
        symbol = tokenizer.advance() #should be }
        self.write("symbol", symbol)
        self.write("</class>\n")

    def CompileClassVarDec(self, tokenizer):
        while tokenizer.current_token == 'static' or tokenizer.current_token == 'field': #as long as there is one more statement
            token = tokenizer.advance()
            self.write_terminal("keyword",token)
            type = tokenizer.advance() #return type
            token_type = Tokenizer.token_type(type)
            self.write_terminal(token_type.lower(),type)



    def CompileSubroutine(self, tokenizer):
        pass

    def CompileParameterList(self, tokenizer):
        pass

    def CompileVarDec(self, tokenizer):
        pass

    def CompileStatements(self,tokenizer):
        pass

    def CompileDo(self,tokenizer):
        pass

    def CompileLet(self,tokenizer):
        pass

    def CompileWhile(self, tokenizer):
        pass
    
    def CompileReturn(self, tokenizer):
        pass

    def CompileIf(self, tokenizer):
        pass

    def CompileExpression(self, tokenizer):
        pass

    def CompileTerm(self, tokenizer):
        pass

    def CompileExpressionList(self, tokenizer):
        pass

    def write_terminal(self,type,string):
        self.write("<"+type+"> "+string+" </"+type+">\n")
