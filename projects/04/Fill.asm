// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@END
0;JMP

(BLACKSCREEN)
@i
M=0 //i=0

@8191
D=A;
@lim
M=D //lim=8191

@zero
M=0 // zero 

@ones
M=-1 // ones has-1

(LOOPA)

@i
D=M //D=i

@lim
D=D-M; //i-8191

@END
D;JGT

@SCREEN
D=A // D contains the address of screen

@i
D=D+M // A=Screen+I

@currentscreen
M=D //stores current row

@ones
D=M;

@currentscreen
A=M // set a TO ADDRESS 
M=D; //mem[a] 

@i
M=M+1; //update the screen address 
@LOOPA
0;JMP



(WHITESCREEN)
@i
M=0 //i=0

@8191
D=A;
@lim
M=D //lim=8191

@zero
M=0 // zero 

@ones
M=-1 // ones has-1

(LOOPB)

@i
D=M //D=i

@lim
D=D-M; //i-8191

@END
D;JGT

@SCREEN
D=A // D contains the address of screen

@i
D=D+M // A=Screen+I

@currentscreen
M=D //stores current row

@zero
D=M;

@currentscreen
A=M // set a TO ADDRESS 
M=D; //mem[a] 

@i
M=M+1; //update the screen address 
@LOOPB
0;JMP

(END)
@KBD  
D=M; //store keyboard in D

@BLACKSCREEN 
D;JNE //go to blackscreen if D is not 0

@WHITESCREEN
D;JEQ