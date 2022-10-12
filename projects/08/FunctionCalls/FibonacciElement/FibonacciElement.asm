//Main
//function Main.fibonacci 0
(Main.fibonacci)
//push argument 0
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
//push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//lt                     // checks if n<2
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
M=-1
@JMPPOINT0
D;JLT
@SP
A=M
M=0
(JMPPOINT0)
@SP
M=M+1
//if-goto IF_TRUE
@SP
M=M-1
A=M
D=M
@Main.fibonacci.IF_TRUE
D;JNE
//goto IF_FALSE
@Main.fibonacci.IF_FALSE
0;JMP
//label IF_TRUE          // if n<2, return n
(Main.fibonacci.IF_TRUE)
//push argument 0
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
//return
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
//label IF_FALSE         // if n>=2, returns fib(n-2)+fib(n-1)
(Main.fibonacci.IF_FALSE)
//push argument 0
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
//push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
//call Main.fibonacci 1  // computes fib(n-2)
@Main.fibonacciRET0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@LCL
M=D
@SP
D=M
@6
D=D-A
@ARG
M=D
@Main.fibonacci
0;JMP
(Main.fibonacciRET0)//push argument 0
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
//push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
//call Main.fibonacci 1  // computes fib(n-1)
@Main.fibonacciRET1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@LCL
M=D
@SP
D=M
@6
D=D-A
@ARG
M=D
@Main.fibonacci
0;JMP
(Main.fibonacciRET1)//add                    // returns fib(n-1) + fib(n-2)
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
//return
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
//Sys
//function Sys.init 0
(Sys.init)
//push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
//call Main.fibonacci 1   // computes the 4'th fibonacci element
@Main.fibonacciRET2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@LCL
M=D
@SP
D=M
@6
D=D-A
@ARG
M=D
@Main.fibonacci
0;JMP
(Main.fibonacciRET2)//label WHILE
(Sys.init.WHILE)
//goto WHILE              // loops infinitely
@Sys.init.WHILE
0;JMP
