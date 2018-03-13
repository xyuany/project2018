import numpy as np
from sklearn import svm
import os
import sys
import pssm as pm
import pickle

###########################################################
###You can change pssm file path by running this script
###########################################################

path = sys.argv[1]

############################################################
###This function is to parse the pssm file
############################################################

def parse_input(path):
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
############################################################
###This function is to encode predicted topology sequence into readable character
############################################################
def topo_rev_encode(result_array):
	encode_table = {1:'C',2:'E',3:'H'}
	result_list = list(result_array)
	topo_list = str()
	for i in result_list:
		topo = encode_table[i]
		topo_list += topo 
	return topo_list
###############################################################
#######Main function
###for each input pssm get a topology
################################################################

pssm = parse_input(path)
clf = pickle.load(open('./logs/model_pssm/pssm_model.sav','rb'))
f = open('./output/output_pssm.txt','w')
for key in pssm:
	pssm_input = dict()
	pssm_input[key] = pssm[key]
	ID_list = sorted(pssm_input.keys())
	X = pm.pssm_window(ID_list, pssm_input,17)
	result = clf.predict(X)
	topo = topo_rev_encode(result)
	f.write('>'+key+'\n')
	#f.write(seq[key]+'\n')
	f.write(topo+'\n')

f.close()
