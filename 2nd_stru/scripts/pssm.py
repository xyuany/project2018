import os
import numpy as np
import sys


path = "./logs/pssm/"
file_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))] 

#print (len(file_list))

def parse_pssm(file_list):
	pssm = dict()
	for f in ['>154l-1-AUTO.1.pssm']:
		#print (f)
		file_array = np.genfromtxt(path+f, skip_header = 3, skip_footer = 5, usecols =range(22,42))
		file_array = file_array/100
		#print (file_array)
		key = f.lstrip('>').rstrip('.pssm')
		pssm[key] = file_array
		#print (pssm)
		return pssm






def main():
	pssm = parse_pssm(file_list)
	
		
if __name__ == '__main__':
	

