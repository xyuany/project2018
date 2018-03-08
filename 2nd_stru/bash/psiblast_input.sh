cd ./logs/seq_file/

echo "program starts running"

for i in *
do
	echo "start running PSI-BLAST on $i"
	psiblast -db /scratch/uniref90.fasta -query $i -out ../align/$i.ali -out_ascii_pssm ../pssm/$i.pssm -num_iterations 2 -num_threads 8 -comp_based_stats 1
	echo "finish running PSI-BALST on $i"
done

echo "Completed"
