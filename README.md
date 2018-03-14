# project2018
------------------------------------------------------------
This repository is to predict 3 state 2nd structure of a protein.
# usage:
--------------------------------------------------------------
## command
--------------------------------------------------------
```Bash
cd ./2nd_stru/	#Bash
```
* to use the predictor successfully, you must in ***/2nd_stru/*** folder
* If you want to run model built by sequence information.
```Bash
 python3 ./script/input_seq.py ./input/input.txt #Bash
```
* Attention:
	* You can change your own test file path in **\<input sequence file>**
* If you want to run model built by pssm.
```Bash
python3 ./script/input_pssm.py ./input/pssm/ #Bash
```
* Attention:
	* You can change your own pssm path in **\<input pssm folder>**, path folder must end with '/'
	* The pssm filename must starts with '>' and end with '.pssm'. For example: \>1hnf-1-AS.pssm

## mandatary file
* ./input/
* ./logs/model_pssm/<br>
* ./logs/model_seq/<br>
* ./script/<br>
* ./output/

## Output
* Output is in ***/2nd_stru/output/***
* ***./output.txt***
	* Prediction by sequence model.
	* Format: 3line.
		* First line: >ID
		* Second line: amino acid sequences
		* Third line: Topology sequences
* ***./output_pssm.txt***
	* Prediction by pssm model.
	* Format: 2line
		* First line: >ID
		* Second line: Topology sequences
	* You can conbine your sequences and predicted topology on your own.


# /2n_stru/ file introduction
## /input/ 
###  /input.txt
 contain a sequence to test<br>
## /script/
### ./input.py  
 the script to run<br>
### ./StruPre.py 
 functions to extract data structures, sliding window, and onehotencode.<br>
### ./traning_tesing_set.py
 manually split dataset into 5-fold.<br>
### ./cross_validation.py
 manually do cross-validation and change parameter <br>
## /logs/
 models and arrays produced during building the predictor.
### ./model/  
 contain the model I have built.<br>
### ./CV_gourp_array
 SVM input array. Use in cross-validation
## /output/
 contain the output file.

