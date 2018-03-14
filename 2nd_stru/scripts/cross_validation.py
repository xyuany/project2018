import numpy as np
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import sys
import StruPre as sp
import training_testing_set as tt
import timeit

inputfile = sys.argv[1]



#################################################################################################
###############load numpy array data
####################################################################################

def load(i):
	load = np.load('./logs/CV_group_array/'+str(i)+'.npz')
	#load = np.load('./logs/CV_pssm_array/'+str(i)+'.npz')
	seq = load['seq_data']
	topo = load['topo_data']
	#print (seq.shape,topo.shape)
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

###############################################################
####This function is to do cross validation
####The input should contain one model
####the return is mean of 5-fold cross validation
#############################################################

def cross_val(seq,topo,model):
	score_array = np.empty((0,))
	for i in range(5):
		test_seq = seq[group[i]]
		test_topo = topo[group[i]]
		train_seq,train_topo = merge_set(seq,topo,i,win_size)
		#print (group[i],test_seq.shape,test_topo.shape)
		model.fit(train_seq,train_topo)
		score = model.score(test_seq,test_topo)
		score_array = np.append(score_array, score)
		#print (score)
	mean = np.average(score_array)
	#print (score_array)
	#print (mean)
	return mean


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

svmhandle = open ("./output/svm.txt",'w')
kernal = ['linear','poly','rbf','sigmoid']
svmhandle.write("win_size\tlinear(C=0.01)\tlinear(C=1)\tlinear(C=100)\tpoly(C=0.01)\tpoly(C=1)\tpoly(C=100)\trbf(C=0.01)\trbf(C=1)\trbf(C=100)\tsigmoid(C=0.01)\tsigmoid(C=1)\tsigmoid(C=100)\t\n")
svmhandle.flush()

rfchandle = open("./output/rfc.txt",'w')
rfchandle.write("win_size\testimator=10(mss=2)\testimator=10(mss=4)\testimator=10(mss=6)\testimator=20(mss=2)\testimator=20(mss=4)\testimator=20(mss=6)\testimator=30(mss=2)\testimator=30(mss=4)\testimator=30(mss=6)\testimator=40(mss=2)\testimator=40(mss=4)\testimator=40(mss=6)\testimator=50(mss=2)\testimator=50(mss=4)\testimator=50(mss=6)\t\n")
rfchandle.flush()

dtchandle = open("./output/dmc.txt",'w')
dtchandle.write("win_size\tauto(mss=2)\tauto(mss=4)\tauto(mss=6)\tNone(mss=2)\tNone(mss=4)\tNone(mss=6)\t\n")
dtchandle.flush()

timehandle = open("./output/time.txt",'w')

for win_size in range(21,23,2):
	# If you want to use sequence information to do cross validation, delete the #
	tt.main(inputfile, win_size)
	# If you want to use pssm information to do cross validation,delete the #
	#tt.pssm_main(inputfile,win_size)
	seq = dict()
	topo = dict()
	group =['G1','G2','G3','G4','G5']
	for i in range(1,6):
		seq[group[i-1]], topo[group[i-1]] = load(i)
	#for para in para_list:
	#following is svm_training
	svmhandle.write(str(win_size)+"\t")
	svmhandle.flush()
	for ker in kernal:
		svm_start = timeit.default_timer()
		for C in [0.01,1,100]:
			clf = svm.SVC(C = C, cache_size=2000, kernel = ker)
			score = cross_val(seq,topo,clf)
			svmhandle.write(str(score)+"\t")
			svmhandle.flush()
		svm_end = timeit.default_timer()
		timehandle.write("svm\t"+str(win_size)+"\t"+ker+"\t"+str(svm_end-svm_start)+"\n")
		timehandle.flush()
	svmhandle.write("\n")
	svmhandle.flush()
	#following is random forest training
	rfchandle.write(str(win_size)+"\t")
	rfchandle.flush()
	for estimator in [10,20,30,40,50]:
		rf_start = timeit.default_timer()
		for mss in [2,4,6]:
			rfc = RandomForestClassifier(n_estimators = estimator, min_samples_split = mss, n_jobs=-1)
			score = cross_val(seq,topo,rfc)
			rfchandle.write(str(score)+"\t")
			rfchandle.flush()
		rf_end = timeit.default_timer()
		timehandle.write("rf\t"+str(win_size)+"\t"+str(estimator)+"\t"+str(rf_end-rf_start)+"\n")
		timehandle.flush()
	rfchandle.write("\n")
	rfchandle.flush()
	#following is decision making trees
	dtchandle.write(str(win_size)+"\t")
	dtchandle.flush()
	for mf in ["auto",None]:
		dm_start = timeit.default_timer()
		for mss in [2,4,6]:
			dtc = DecisionTreeClassifier(max_features = mf, min_samples_split = mss)
			score = cross_val(seq,topo,dtc)
			dtchandle.write(str(score)+"\t")
			dtchandle.flush()
		dm_end = timeit.default_timer()
		timehandle.write("dm\t"+str(win_size)+"\t"+str(mf)+"\t"+str(dm_end-dm_start)+"\n")
		timehandle.flush()
	dtchandle.write("\n")
	dtchandle.flush()

svmhandle.close()
rfchandle.close()
dtchandle.close()
timehandle.close()
