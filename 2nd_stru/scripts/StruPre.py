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
	for key in seq_stru:
		b.update(seq_stru[key])
	b = list(b)
	b.sort()
	print (b)

def uniq_topo(topo_stru):
	a = set()
	for key in topo_stru:
		a.update(topo_stru[key])
	a = list(a)
	a.sort()
	print (a)


inputfile = sys.argv[1]

seq, topo = data_stru(inputfile)

uniq_aa(seq)
uniq_topo(topo)
