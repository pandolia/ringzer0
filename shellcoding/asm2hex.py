# usage:
# python asm2hex
# > mov rsp, 0
# 48 bc 00 00 00 00 00 00 00 00

import os, time

while True:
    s = raw_input('> ')
    if not s:
        break
    tempasm = file('temp/temp.asm', 'w')
    tempasm.write('_start:\n\t' + s + '\n')
    tempasm.close()
    time.sleep(0.01)
    os.system(r"nasm -f elf64 temp/temp.asm; objdump -D temp/temp.o -M intel | grep '^ ' | cut -f2-3 > temp/temp.x.asm")
    time.sleep(0.01)
    tempxasm = file('temp/temp.x.asm')
    print tempxasm.read().strip()
    tempxasm.close()
