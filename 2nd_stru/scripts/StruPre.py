import numpy as np
import sys
import getopt
from sklearn import svm
np.set_printoptions(threshold = np.inf)
#from sklearn.externals import joblib
import pickle

'''def getcommand(argv):
	inputfile = ""
	outputfile = ""
	try:
		#parce of command line, h-help, i:-input, change following if add 
		opts, args = getopt.getopt(argv,"hi:")	
	except getopt.GetoptError:
		print ("StruPre.py -i <inputfile>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('test.py -i <inputfile>')
			sys.exit()
		elif opt == '-i':
			inputfile = arg
	return inputfile

inputfile = getcommand(sys.argv[1:])
print (inputfile)'''




def data_stru(inputfile):
	inputhandle = open(inputfile, 'r')
	seq_stru = dict()
	topo_stru = dict ()
	for line in inputhandle:
		line = line.rstrip('\n')
		if line.startswith('>'):
			key = line.lstrip('>')
			count = 1
		elif count == 1:
			seq_stru[key] = line
			count +=1
		elif count == 2:
			topo_stru[key] = line
			count == 0
	inputhandle.close()
	return seq_stru,topo_stru
	
def uniq_aa(seq_stru):
	b = set()
	seq_encode = dict()
	# get unique amino acid
	'''for key in seq_stru:
		b.update(seq_stru[key])
	b = list(b)
	b.sort()
	print (b)'''
	encode = 0
	# encode sorted amino acid into dictionary(number)
	for i in 'ACDEFGHIKLMNPQRSTVWY':
		encode +=1
		seq_encode[i] = encode
	#print (seq_encode)
	return (seq_encode)		

def uniq_topo(topo_stru):
	a = set()
	topo_encode = dict()
	# get unique topology state
	'''for key in topo_stru:
		a.update(topo_stru[key])
	a = list(a)
	a.sort()
	#print (a)'''
	encode = 0
	for i in 'CEH':
		encode +=1
		topo_encode[i] = encode
	#print (topo_encode)
	return (topo_encode)

def seq_encoded(seq_dic,seq_table):
	# iterate each sequence
	for key in seq_dic:
		#print (key,'\n',seq_dic[key])
		seq_encoded = list()
		# iterate each aa to encode into number
		for i in seq_dic[key]:
			seq_encoded.append(seq_table[i])
		#print (seq_encoded)
		# change value of seq_dic: string->list of encoded number
		seq_dic[key] = seq_encoded
		#print(seq_dic)
	return seq_dic

def topo_encoded(topo_dic,topo_table):
	#iterate each sequence
	for key in topo_dic:
		#print (key,'\n',topo_dic[key])
		topo_encoded = list()
		for i in topo_dic[key]:
			topo_encoded.append(topo_table[i])
		#print (topo_encoded)
		topo_dic[key] = topo_encoded
		#print (topo_dic)
	return topo_dic

'''def sliding_window(ID_list, seq_dic, topo_dic, win_size):
	X = list()
	Y = list()
	for key in ID_list:
		topo = topo_dic[key]
		seq = seq_dic[key]
		pos = win_size//2
		#print(seq)
		for i in range(len(seq)):
			prefix = i - pos
			suffix = i + pos + 1 - len(topo)
			if prefix < 0:
				win = [0]*abs(prefix) + seq[i+pos-prefix-win_size+1:i+pos+1]
				# print (win)
			elif suffix >0:
				win = seq[i-pos:i+pos+1]+[0] * suffix
				# print (win)
			else:
				win = seq[i-pos:i+pos+1]
				#print (win)
			X.append(win)
		#print (X)
		Y += topo
	#print (Y)
	return X,Y'''

def seq_sliding_window(ID_list, seq_dic, win_size):
	X = list()
	#Y = list()
	for key in ID_list:
		#topo = topo_dic[key]
		seq = seq_dic[key]
		pos = win_size//2
		#print(seq)
		for i in range(len(seq)):
			prefix = i - pos
			suffix = i + pos + 1 - len(seq)
			if prefix < 0:
				win = [0]*abs(prefix) + seq[i+pos-prefix-win_size+1:i+pos+1]
				# print (win)
			elif suffix >0:
				win = seq[i-pos:i+pos+1]+[0] * suffix
				# print (win)
			else:
				win = seq[i-pos:i+pos+1]
				#print (win)
			X.append(win)
		#print (X)
		#Y += topo
	#print (Y)
	return X


def topo_sliding_window(ID_list,topo_dic):
	Y = list()
	for key in ID_list:
		topo = topo_dic[key]
		Y += topo
	Y = np.array(Y)
	return Y

def varify_length(seq,seq_num,topo,topo_num,X):
	seq_len, seq_num_len, topo_len, topo_num_len,X_len = 0,0,0,0,0
	for key in seq:
		seq_len += len(seq[key])
		seq_num_len += len(seq_num[key])
		topo_len += len(topo[key])
		topo_num_len += len(topo_num[key])
		print (seq_len,seq_num_len,topo_len,topo_num_len)
	X_len = len(X)
	print (X_len)

def seq_binary_table(seq_table):
	binary = np.eye(20)
	seq_binary_table = dict()
	for i in range(20):
		seq_binary_table[i+1] = list(binary[i])
	seq_binary_table[0] = list(np.zeros((20)))
	#print (seq_binary_table)
	return seq_binary_table

def onehotencode(seq_win, binary_table):
	#print (len(X))
	X = list()
	for i in seq_win:
		win_array = list()
		for j in i:
			array = binary_table[j]
			win_array +=array
			#print (len(win_array))
		X.append(win_array)
		#print (len(X[seq_win.index(i)]))
	#print (len(X))
	return X


# main function
#inputfile = sys.argv[1]
#win_size = int(sys.argv[2])
# build data structure: sequence, topology
#seq, topo = data_stru(inputfile)
#print (seq,topo)

def main(seq,topo,win_size):
######build numerical encode table'
	seq_encode_table = uniq_aa(seq)
	topo_encode_table = uniq_topo(topo)
#print (seq_encode_table,topo_encode_table)
#####sorted the input ID
	ID_list = sorted(seq.keys())
#######encode sequences into number'
	seq_num = seq_encoded(seq,seq_encode_table)
	topo_num = topo_encoded(topo,topo_encode_table)

#print (seq_num,topo_num)
#####building sliding window due to sorted ID_list
#####So the sequences order is same 
	#seq_window,Y = sliding_window(ID_list, seq_num, topo_num, win_size)
	seq_window = seq_sliding_window(ID_list, seq_num, win_size)
	Y = topo_sliding_window(ID_list, topo_num)
#seq_window = np.array(X)
	#Y = np.array(Y)
#print (seq_window,Y)
######building one hot encode table '
	binary_table = seq_binary_table(seq_encode_table)
#print (binary_table)
######transform numerical number into 20 binary code'
	X = onehotencode(seq_window, binary_table)
	X = np.array(X)
	return X,Y

#########################################################################
############This function is only for input query sequences
############Deal with sample only have sequences information, no topology\
#########################################################################


def input_main(seq,win_size):
	seq_encode_table = uniq_aa(seq)
	ID_list = sorted(seq.keys())
	seq_num = seq_encoded(seq,seq_encode_table)
	seq_window = seq_sliding_window(ID_list, seq_num, win_size)
	binary_table = seq_binary_table(seq_encode_table)
	X = onehotencode(seq_window, binary_table)
	X = np.array(X)
	return X


#print (X,Y)
#varify_length(seq,seq_num,topo,topo_num,X)
'''clf = svm.SVC()
clf.fit(X,Y)
score = clf.score(X,Y)
print (score)
'''
if __name__ == '__main__':
	X,Y = main(seq,topo,win_size)
	#print (X)
	#print (Y)
	'''clf = svm.SVC()
	clf.fit(X,Y)
	pickle.dump(clf,open('./logs/model/test_model.sav','wb'))'''
