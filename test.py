import cPickle,glob,os,time
import numpy as np
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

from keras import backend as K
import tensorflow as tf


sess_config = tf.ConfigProto(
        allow_soft_placement=True,
        # log_device_placement=True,
        # inter_op_parallelism_threads=8,
        # intra_op_parallelism_threads=8,
        # device_count={'GPU': 0}
        # device_count={'CPU': 0}
    )

sess_config.gpu_options.allow_growth = True
# sess_config.gpu_options.per_process_gpu_memory_fraction = 0.8

sess=tf.Session(config=sess_config)

K.set_session(sess)

from Board import Board
BLACK=0
WHITE=1
NOCHESS=2

os.chdir("output")
files=glob.glob("*.pkl")
for file in files:
    if file=="0.pkl":
        continue
    # print file
    # print os.path.exists(file)
    with open(file,'r')as f:
        data=cPickle.load(f)
        if len(data[-1])==1:
            data[-1]=[]
        else:
            data.append([])
        for item in data:
            item3=item[-1]
            item3=np.array(item3)
            for item3_item in item3.ravel():
                pass


