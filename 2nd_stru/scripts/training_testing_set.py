import numpy as np
from sklearn import svm
import sys
import StruPre as sp
import pssm as pm

inputfile = sys.argv[1]
win_size = int(sys.argv[2])



# build 5-fold cross validation 
#print (length, interval)

#ID_list = sorted(seq.keys())

#print (ID_list)
''' get different testing ID of 5-fold cross validation'''

###########################################################################
##########This function is to seperate whole dataset into 5 parts
###########Group[i] is test_set[i], and it has order
###########################################################################
def test_set(ID_list,interval):
	test_set = list()
	for i in range(5):
		if i == 4:
			test_ID = ID_list[interval*i:]
			test_set.append(test_ID)
		else:
			test_ID = ID_list[interval*i:interval*(i+1)]
			test_set.append(test_ID)
		#print (len(test_set[i]))
	return test_set

#############################################################################
###########This function is to get seq_dictionary and topo_dictionary in each group
############Use main() in 'StruPre.py' to convert into binary array and save in 'i.npz'
############ main() will sort keys of input dictionary and return have fixed order
##################################################################################


def train_test_set(test_list,seq_dic,topo_dic,win_size):
	#train_list = list (set(ID_list) - set(test_list))
	#print (len(test_list))
	for i in range(len(test_list)):
		group_seq = list_dic(test_list[i],seq_dic)
		group_topo = list_dic(test_list[i],topo_dic)
		X,Y = sp.main(group_seq,group_topo,win_size)
		np.savez("./logs/CV_group_array/"+str(i+1),seq_data = X, topo_data = Y)
		#print (X.shape,Y.shape)
	
def list_dic(ID_list,all_dic):
	ID_dict = dict()
	for i in ID_list:
		#print (i)
		ID_dict[i] = all_dic[i]
	return ID_dict

def pssm_train_test_set(test_list,pssm_dic,topo_dic,win_size):
	#train_list = list (set(ID_list) - set(test_list))
	#print (len(test_list))
	for i in range(len(test_list)):
		group_pssm = list_dic(test_list[i],pssm_dic)
		group_topo = list_dic(test_list[i],topo_dic)
		X,Y = pm.main(group_pssm,group_topo,win_size)
		#np.savez("./logs/CV_pssm_array/"+str(i+1),seq_data = X, topo_data = Y)
		print (X.shape,Y.shape)


def main(inputfile,win_size):
	seq, topo = sp.data_stru(inputfile)
	length = len(seq)
	interval = length//5
	ID_list = sorted(seq.keys())
	test_group = test_set(ID_list,interval)
	train_test_set(test_group,seq,topo,win_size)	

def pssm_main(inputfile,winsize):
	seq, topo = sp.data_stru(inputfile)
	pssm = pm.parse_pssm()
	if topo.keys() == pssm.keys():
		print (True)
	else:
		print (topo.keys()-pssm.keys())
	#print (pssm)
	length = len(pssm)
	interval = length//5
	ID_list = sorted(pssm.keys())
	test_group = test_set(ID_list,interval)
	pssm_train_test_set(test_group,pssm,topo,win_size)

if __name__ == '__main__':
	#main(inputfile, win_size)
	pssm_main(inputfile, win_size)
#print (test_set)
