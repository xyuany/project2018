import os
import numpy as np
import sys
import StruPre as sp
from sklearn import svm
import pickle


#####################################################################
###Extract pssm and normalize it from files
#####################################################################

def parse_pssm():
#################################################
#####You can change pssm files' path here
################################################
	path = "./logs/pssm/"
	file_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))] 
	#print (len(file_list))
	pssm = dict()
	for f in file_list:
		#print (f)
		file_array = np.genfromtxt(path+f, skip_header = 3, skip_footer = 5, usecols =range(22,42))
		file_array = file_array/100
		#print (file_array.shape)
		key = f.lstrip('>').rstrip('pssm').rstrip('.')
		pssm[key] = file_array
	#print (sorted(pssm.keys()))
	return pssm


def pssm_window(ID_list, pssm_array,win_size):
	position = win_size//2
	X = np.empty((0,win_size*20))
	#print (X.shape)
	for key in ID_list:
		#print (key)
		pssm_seq = pssm_array[key]
		#print (pssm_seq.shape)
		for i in range(len(pssm_seq)):
			#print (len(pssm_seq))
			prefix = i - position
			suffix = i + position + 1 - len(pssm_seq)
			if prefix <0:
				zero = np.zeros(20*abs(prefix))
				win_array = np.append(zero,pssm_seq[i+position-prefix-win_size+1:i+position+1,])
				#print(win_array.shape)
			elif suffix >0:
				zero = np.zeros(20*abs(suffix))
				win_array = np.append(pssm_seq[i-position:,],zero)
				#print(win_array.shape)
			else:
				win_array = pssm_seq[i-position:i+position+1].flatten()
			win_array = win_array.reshape(1,win_size*20)
			X = np.append(X, win_array, axis = 0)
			#print (win_array.shape)
		#print (X.shape)
	return X

###########################################################
####If you want to run this script seperately 
####Delete the comment
####In other cases, you should comment following hard code 
###########################################################
'''
inputfile = sys.argv[1]
win_size = int(sys.argv[2])
pssm = parse_pssm()
#print (pssm)
seq, topo = sp.data_stru(inputfile)
'''

def main(pssm,topo,win_size):
	ID_list = sorted(pssm.keys())
	X = pssm_window(ID_list, pssm, win_size)
	#print (X.shape)
	topo_encode_table = sp.uniq_topo(topo)
	topo_num = sp.topo_encoded(topo,topo_encode_table)
	Y = sp.topo_sliding_window(ID_list,topo_num)
	#print (Y.shape)
	return X,Y


def fit_model(X,Y):
	clf = svm.SVC(C = 100, kernel = 'rbf',cache_size = 2000)
	clf.fit(X,Y)
	pickle.dump(clf,open('./logs/model_pssm/pssm_model.sav','wb'))
	print ('Done')

if __name__ == '__main__':
	X,Y = main(pssm,topo,win_size)
	#################################
	####Delete # if want to save model
	#################################
	#fit_model(X,Y)
