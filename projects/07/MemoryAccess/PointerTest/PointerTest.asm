@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// pushed D to stack 
// completed a push 
@R3
D=A
@0
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
// popped stack to D 
@R13
A=M
M=D
// completed a pop 
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
// pushed D to stack 
// completed a push 
@R3
D=A
@1
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
// popped stack to D 
@R13
A=M
M=D
// completed a pop 
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// pushed D to stack 
// completed a push 
@R3
D=M
@2
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
// popped stack to D 
@R13
A=M
M=D
// completed a pop 
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// pushed D to stack 
// completed a push 
@R4
D=M
@6
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
// popped stack to D 
@R13
A=M
M=D
// completed a pop 
@R3
D=A
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushed D to stack 
// completed a push 
@R3
D=A
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushed D to stack 
// completed a push 
@SP
M=M-1
A=M
D=M
// popped stack to D 
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
@R3
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushed D to stack 
// completed a push 
@SP
M=M-1
A=M
D=M
// popped stack to D 
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
@R4
D=M
@6
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pushed D to stack 
// completed a push 
@SP
M=M-1
A=M
D=M
// popped stack to D 
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
