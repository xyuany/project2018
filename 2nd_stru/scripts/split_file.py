import sys
filehandle = open(sys.argv[1],'r')
for line in filehandle:
	if line.startswith('>'):
		line = line.rstrip('\n')
		count = 1
		writehandle = open('./logs/seq_file/'+line,'w')
		writehandle.write(line+'\n')
	elif count == 1:
		writehandle.write(line)
		count = 0
		writehandle.close()
filehandle.close()
