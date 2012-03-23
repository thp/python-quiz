swig -python roman.i
gcc -shared -o _roman.so -O3 -fPIC roman_wrap.c `python-config --libs --cflags`
gcc -o roman -O3 roman.c
#rm _roman.so roman roman.py roman_wrap.c
