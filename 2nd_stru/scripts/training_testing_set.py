import numpy as np
from sklearn import svm
import sys
import StruPre as sp

inputfile = sys.argv[1]
win_size = int(sys.argv[2])

seq, topo = data_stru(inputfile)
length = len(seq)
