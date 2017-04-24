import subprocess
import os
print os.getcwd()
subprocess.call(["sh","./make.sh"])
from ctypes import *
from ctypes.util import *
from Board import *
import numpy as np
from numpy.ctypeslib import  ndpointer

mtcs_lib=CDLL("./mtcs.so")
# mtcs_lib.myprint.restype = c_char_p
# print mtcs_lib.myprint()

board_arr=[[None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, 'w', 'b', None, None, None], [None, None, None, 'b', 'w', None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
board_arr=np.array(board_arr)
for i,row in enumerate(board_arr):
    for j,col in enumerate(row):
        if col is None:
            board_arr[i,j]=2
        elif col == 'w':
            board_arr[i,j]=0
        else:
            board_arr[i,j]=1

board_arr=board_arr.ravel().astype("int32")
mtcs_lib.getNextPosition3.argtypes=[
    ndpointer(c_int),c_int
]
mtcs_lib.getNextPosition3.restype = ndpointer(dtype=c_int,shape=(2,))

res= mtcs_lib.getNextPosition3(
    np.ascontiguousarray(board_arr),0
)
print res


