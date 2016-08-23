# Additional scripts

Scripts used to perform analyses reported in the LSTrAP manuscript (Proost et al., *under preparation*) are found in 
*./helper*

## htseq_count_stats.py and tophat_stats.py

These scripts will extract the statistics used to assess the quality of samples. 

    python3 htseq_count_stats.py ./path/to/htseq/files > output.txt
    python3 tophat_stats.py ./path/to/tophat/output > output.txt
    
## pca_powerlaw.py

Script to perform a PCA analysis on the *Sorghum bicolor* data (case study) and draw the node degree distribution. The
required data is included here as well. Note that this script requires sklearn and seaborn.

    python3 pca_powerlaw.py ./data/sbi.expression.matrix.tpm.txt ./data/sbi_annotation.txt ./data/sbi.power_law.R07.txt
    
## get_sra_ip.py

Script to download runs from [Sequence Read Archive](http://www.ncbi.nlm.nih.gov/sra), requires the Aspera connect 
client to be installed and a open ssh key is required (can be obtained from the Apera connect package)
 
    python3 get_sra_ip.py runs.list.txt ./output/directory /absolute/path/to/opensshkey
     
## sra_to_fastq.py

Script to convert sra files into fastq. Sratools is required.

    python3 sra_to_fastq.py /sra/files/directory /fastq/output/directory
    
