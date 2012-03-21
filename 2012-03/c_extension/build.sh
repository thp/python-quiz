swig -python roman.i
gcc -shared -o _roman.so -O3 -fPIC roman_wrap.c -I/usr/include/python2.7
gcc -o roman -O3 roman.c
#rm _roman.so roman roman.py roman_wrap.c
