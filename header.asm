
use 16;
org 0xfffffff0;
	jmp 0x0000:24576;
org 0x6000;
    mov eax, 0x922f3aef;
    mov edx, 0x4d4653e3;
    mov ecx, 0x1523;
    wrmsr;
    mov eax, 0x3ff00000;
    mov edx, 0x0;
    mov ecx, 0x317B;
    rdmsr;
