import numpy as np
from sklearn import svm
import sys
import StruPre as sp
import pssm as pm
import pickle
from sklearn.metrics import classification_report

path = sys.argv[1]
inputfile = sys.argv[2]
f = open('./output/50test/50test_output.txt','w')

seq, topo = sp.data_stru(inputfile)
seq_model = pickle.load(open('./logs/model_seq/seq_model.sav','rb'))
X, Y_real = sp.main(seq,topo,19)
Y_predict = seq_model.predict(X)
target_names = ['class 0', 'class 1', 'class 2']

f.write(classification_report(Y_real, Y_predict, target_names=target_names))

f.write('\n\n')

ID_list = sorted(topo.keys())
pssm_model = pickle.load(open('./logs/model_pssm/pssm_model.sav','rb'))
pssm = pm.parse_pssm(path)
PSSM = pm.pssm_window(ID_list, pssm, 17)
PSSM_predict = pssm_model.predict(PSSM)
f.write(classification_report(Y_real, PSSM_predict, target_names = target_names))

f.close()
