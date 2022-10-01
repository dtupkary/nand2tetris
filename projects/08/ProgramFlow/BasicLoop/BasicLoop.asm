//BasicLoop
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pushed D to stack 
// completed a push 
@R1
D=M
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
(.LOOP_START)
@R2
D=M
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
@R1
D=M
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
@R1
D=M
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
@R2
D=M
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
@1
D=A
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
@R2
D=M
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
@R2
D=M
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
@SP
M=M-1
A=M
D=M
// popped stack to D 
@.LOOP_START
D;JNE
@R1
D=M
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
