// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

@i
M=1 //stores count

@R2
M=0 // stores sum

(LOOP)

@i
D=M // D stores curernt value of i
@R1
D=D-M; // D stores current value of i-R1

@END
D;JGT // jump is mult is done.

@R2
D=M // D is current value of sum

@R0
D=D+M // D=sum+R0

@R2
M=D //store in sum

@i 
M=M+1 //increment i. 

@LOOP
0;JMP 






(END)

@END
0;JMP

