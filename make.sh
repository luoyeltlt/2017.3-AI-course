rm *.o  *.so -f

#gcc  -shared  -Wl,-soname,ex2  -o ex2.so -fPIC ex2.cpp -lstdc++ -lpython2.7
gcc  -shared  -Wl,-soname,ex2  -o mtcs.so -fPIC mtcs.cpp -lstdc++ -lpython2.7

#swig -tcl example.i
#swig -python example.i
#gcc -c example.c example_wrap.c -I/usr/local/include/python2.7 -fPIC
#ld -shared example.o example_wrap.o -o _example.so

