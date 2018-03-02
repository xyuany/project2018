import numpy as np
from sklearn import svm
import sys
import StruPre as sp
import training_testing_set as tt

inputfile = sys.argv[1]



#################################################################################################
###############load numpy array data
####################################################################################

def load(i):
	load = np.load('./logs/CV_group_array/'+str(i)+'.npz')
	seq = load['seq_data']
	topo = load['topo_data']
	return seq, topo

#####################################################################
#################Merge other group except testing set
#####################################################################



def merge_set(seq_group, topo_group, i, win_size):
	group =['G1','G2','G3','G4','G5']
	training_seq = np.empty((0,win_size*20))
	training_topo = np.empty((0,))
	for j in range(5):
		if i != j:
			#print (training_seq.shape, seq_group[group[j]].shape)
			training_seq = np.append(training_seq,seq_group[group[j]],axis = 0)
			training_topo = np.append(training_topo, topo_group[group[j]])
	return training_seq, training_topo
	

#####################################################################
####################Test part
######################################################################	
'''group =['G1','G2','G3','G4','G5']
a = np.array([[1,1]])
b = np.array([[2,2]])
c = np.array([[3,3]])
d = np.array([[4,4]])
e = np.array([[5,5]])

seq_test = {'G1':a,'G2':b,'G3':c,'G4':d,'G5':e}
topo_test = {'G1':a,'G2':b,'G3':c,'G4':d,'G5':e}

for i in range(5):
	test_seq = seq_test[group[i]]
	test_topo = topo_test[group[i]]
	train_seq,train_topo = merge_set(seq_test,topo_test,i,2)
	print (group[i],test_seq,test_topo)
	print (group[i],train_seq,train_topo)	
'''



for win_size in range(5,7,2):
	tt.main(inputfile, win_size)
	seq = dict()
	topo = dict()
	group =['G1','G2','G3','G4','G5']
	for i in range(1,6):
		seq[group[i-1]], topo[group[i-1]] = load(i)
	#for para in para_list:
	clf = svm.SVC()
	for i in range(5):
		test_seq = seq[group[i]]
		test_topo = topo[group[i]]
		train_seq,train_topo = merge_set(seq,topo,i,win_size)
		#print (group[i],test_seq.shape,test_topo.shape)
		clf.fit(train_seq,train_topo)
		score = clf.score(test_seq,test_topo)
		print (score)
		

