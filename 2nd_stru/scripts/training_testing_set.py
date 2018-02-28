import numpy as np
from sklearn import svm
import sys
import StruPre as sp

inputfile = sys.argv[1]
win_size = int(sys.argv[2])

seq, topo = sp.data_stru(inputfile)
length = len(seq)
interval = length//5

# build 5-fold cross validation 
#print (length, interval)

ID_list = sorted(seq.keys())

print (ID_list)
''' get different testing ID of 5-fold cross validation'''


def test_set(ID_list):
	test_set = list()
	for i in range(5):
		if i == 4:
			test_ID = ID_list[interval*i:]
			test_set.append(test_ID)
		else:
			test_ID = ID_list[interval*i:interval*(i+1)]
			test_set.append(test_ID)
	#print (test_set)
	return test_set

''' extract training and testing data from total data 
	get results as dictionary
	by test_set[list]''' 

def train_test_set(test_list,ID_list,seq_dic,topo_dic):
	train_list = list (set(ID_list) - set(test_list))
	train_seq = list_dic(train_list,seq_dic)
	train_topo = list_dic(train_list,topo_dic)
	test_seq = list_dic(test_list,seq_dic)
	test_topo = list_dic(test_list,topo_dic)
	return train_seq, train_topo, test_seq, test_topo
	
def list_dic(ID_list,all_dic):
	ID_dict = dict()
	for i in ID_list:
		ID_dict[i] = all_dic[i]
	return ID_dict




test_set = test_set(ID_list)
train_test_set(test_set[0],ID_list,seq,topo)
