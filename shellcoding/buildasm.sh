#/bin/bash
# usage: ./buildasm.sh ch133
mkdir -p $1-build
cd $1-build
nasm -f elf64 ../$1.asm -o $1.o
ld -N -s -o $1 $1.o
objdump -D $1.o | grep '^ ' | cut -f2 \
| tr -d $'\x0a\x20' | \
sed 's_[a-z0-9][a-z0-9]_\\x&_g' > $1.payload
objdump -D $1 -M intel > $1.x.asm
