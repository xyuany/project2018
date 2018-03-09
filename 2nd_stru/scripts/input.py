import numpy as np
from sklearn import svm
import sys
import getopt
import StruPre as sp
#from sklearn.externals import joblib
import pickle

inputfile = sys.argv[1]


def input_structure(inputfile):
	input_handle = open(inputfile,'r')
	seq_stru = dict()
	for line in input_handle:
		line = line.rstrip('\n')
		if line.startswith('>'):
			key = line.lstrip('>')
		else:
			seq_stru[key] = line
	input_handle.close()
	return seq_stru

def topo_rev_encode(result_array):
	encode_table = {1:'C',2:'E',3:'H'}
	result_list = list(result_array)
	topo_list = str()
	for i in result_list:
		topo = encode_table[i]
		topo_list += topo 
	return topo_list

#seq = input_structure(inputfile)
#topo = dict()
seq = input_structure(inputfile)
clf = pickle.load(open('./logs/model/test_model.sav','rb'))
f = open('./output/output.txt','w')
for key in seq:
	seq_input = dict()
	seq_input[key]=seq[key]
	X = sp.input_main(seq_input,5)
	result = clf.predict(X)
	topo = topo_rev_encode(result)
	f.write('>'+key+'\n')
	f.write(seq[key]+'\n')
	f.write(topo+'\n')
f.close()
#print (X)
#print (Y)
#print (str(topo))
