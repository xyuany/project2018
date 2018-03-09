# project2018
3 state 2nd structure prediction

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
# usage
## command
* cd ./2nd_stru/	#to use the predictor successfully, you must in /2nd_stru/ folder
* #then run 
* $ python3 ./script/input.py \<input sequence>
## mandatary file
* ./script/input.py<br>
* ./script/PreStru.py<br>
* ./logs/model/<br>
* ./input/input.txt
