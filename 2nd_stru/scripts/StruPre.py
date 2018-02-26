import numpy as np
import sys
import getopt

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



inputfile = sys.argv[1]
#print (inputfile)

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
	return seq_stru,topo_stru
	
def uniq_aa(seq_stru):
	b = set()
	seq_encode = dict()
	# get unique amino acid
	for key in seq_stru:
		b.update(seq_stru[key])
	b = list(b)
	b.sort()
	#print (b)
	encode = 0
	# encode sorted amino acid into dictionary(number)
	for i in b:
		encode +=1
		seq_encode[i] = encode
	#print (seq_encode)
	return (seq_encode)		

def uniq_topo(topo_stru):
	a = set()
	topo_encode = dict()
	# get unique topology state
	for key in topo_stru:
		a.update(topo_stru[key])
	a = list(a)
	a.sort()
	#print (a)
	encode = 0
	for i in a:
		encode +=1
		topo_encode[i] = encode
	#print (topo_encode)
	return (topo_encode)


inputfile = sys.argv[1]

seq, topo = data_stru(inputfile)

seq_encode_table = uniq_aa(seq)
topo_encode_table = uniq_topo(topo)
print (len(seq_encode_table), len(topo_encode_table))
