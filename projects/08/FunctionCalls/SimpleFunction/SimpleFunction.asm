//SimpleFunction
(SimpleFunction.test)
D=0
@SP
A=M
M=D
@SP
M=M+1
// pushed D to stack 
D=0
@SP
A=M
M=D
@SP
M=M+1
// pushed D to stack 
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
@R1
D=M
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
@SP
M=M-1
@SP
A=M
M=!M
@SP
M=M+1
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
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
@R2
D=M
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
M=M-D
@SP
M=M+1
@LCL
D=M
@R14
M=D
@R14
D=M
@5
D=D-A
A=D
D=M
@R15
M=D
@SP
M=M-1
A=M
D=M
// popped stack to D 
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R14
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@R14
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@R14
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@R14
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@R15
A=M
0;JMP
