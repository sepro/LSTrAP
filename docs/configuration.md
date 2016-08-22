# Configuring LSTrAP
## config.ini
In your config file module names need to be specified. To see which modules are available on your system type:

    module avail

Add the module name for each of the tools to your config.ini, also update the path to Trimmomatic.
In case the module load system isn't used, but all software is installed on the cluster + nodes set the modules to **None** !

In case you would like to tweak parameters passed to tools this would be the place to do so. Note however that the tools
will run with the same settings for each file. Modifying parameters that would **change the output name or format will 
cause the pipeline to break**. Arguments with a name like *${var}* should **not** be changed as this is how the pipeline 
defines the input and output for each tool.

Example config.ini:

```ini
[TOOLS]
; In case there is no module load system on the system set the module name to None

trimmomatic_path=/home/sepro/tools/Trimmomatic-0.36/trimmomatic-0.36.jar

; Module names
bowtie_module=biotools/bowtie2-2.2.6
samtools_module=biotools/samtools-1.3
sratoolkit_module=biotools/sratoolkit-2.5.7
tophat_module=biotools/tophat-2.1.0

interproscan_module=biotools/interproscan-5.16-55.0

blast_module=biotools/ncbi-blast-2.3.0+
mcl_module=biotools/mcl-14.137

python_module=devel/Python-2.7.10

; commands to run tools
bowtie_cmd=bowtie2-build ${in} ${out}

trimmomatic_se_command=java -jar ${jar} SE -threads 1  ${in} ${out}  ILLUMINACLIP:/home/sepro/tools/Trimmomatic-0.36/adapters/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
trimmomatic_pe_command=java -jar ${jar} PE -threads 1  ${ina} ${inb} ${outap} ${outau} ${outbp} ${outbu} ILLUMINACLIP:/home/sepro/tools/Trimmomatic-0.36/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36

tophat_se_cmd=tophat -p 3 -o ${out} ${genome} ${fq}
tophat_pe_cmd=tophat -p 3 -o ${out} ${genome} ${forward},${reverse}

samtools_cmd=samtools view -h -o ${out} ${bam}
htseq_count_cmd=htseq-count -s no -t ${feature} -i ${field} ${sam} ${gff} > ${out}

interproscan_cmd=interproscan.sh -i ${in_dir}/${in_prefix}${SGE_TASK_ID} -o ${out_dir}/${out_prefix}${SGE_TASK_ID} -f tsv -dp -iprlookup -goterms --tempdir /tmp

```

## data.ini
The location of your data needs to be defined in your data.ini file.

Example data.ini file:
```ini
[GLOBAL]
; add all genomes, use semi-colons to separate multiple cfr. zma;ath
genomes=zma

; enter email to receive status updates from the cluster
; setting the email to None will disable this
email=None

; orthofinder settings (runs on all species)
orthofinder_output=./output/orthofinder

[zma]
cds_fasta=
protein_fasta=
genome_fasta=
gff_file=

gff_feature=CDS
gff_id=Parent

fastq_dir=./data/zma/fastq

tophat_cutoff=65
htseq_cutoff=40

bowtie_output=./output/bowtie-build/zma
trimmomatic_output=./output/trimmed_fastq/zma
tophat_output=./output/tophat/zma
samtools_output=./output/samtools/zma
htseq_output=./output/htseq/zma

exp_matrix_output=./output/zma/exp_matrix.txt
exp_matrix_tpm_output=./output/zma/exp_matrix.tpm.txt
exp_matrix_rpkm_output=./output/zma/exp_matrix.rpkm.txt
interpro_output=./output/interpro/zma

pcc_output=./output/zma/pcc.std.txt
pcc_mcl_output=./output/zma/pcc.mcl.txt
```