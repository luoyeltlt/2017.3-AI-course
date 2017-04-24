import subprocess
subprocess.call(["sh","./make.sh"])
from ctypes import *
from ctypes.util import *
for lib_name,lib_path_p in \
        zip(["linux-vdso","c","/lib64/ld-linux-x86-64"],
            ["linux-vdso.so.1","","/lib64/ld-linux-x86-64.so.2"]):
    lib_path=find_library(lib_name)
    if lib_path is None:
        lib_path=lib_path_p
    # print lib_path
    _=CDLL(lib_path)

ex=CDLL("./mtcs.so")
print ex.myprint()#,ex.fact(10)