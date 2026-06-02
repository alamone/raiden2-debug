cpu 8086
cpu 186
 
org 0xB5510
 push bp
 mov bp,sp
 sub sp,8h
 test word [0x9DC2], 0x0080
 jz skip
 mov word [0x9DC0], 0       ; clear P1 joystick-centered state
 mov word [0x9DC2], 0       ; clear P2 joystick-centered state
 push 0
 push 0x1126
 push 0x1183
 call far 0x9800:0x3C04
 pop cx
skip:
 jmp 0x9800:0x0F13
