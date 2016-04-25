# RSTrAP
Rna Seq Transcriptome Analysis Pipeline

## Requirements
RSTrAP wraps multiple existing tools into a single workflow. To use RSTrAP the following tools need to be installed

  * [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)
  * [tophat](https://ccb.jhu.edu/software/tophat/manual.shtml)
  * [samtools](http://www.htslib.org/)
  * [sratools](http://ncbi.github.io/sra-tools/)
  * [python 2.7](https://www.python.org/download/releases/2.7/) + [HTSeq](http://www-huber.embl.de/users/anders/HTSeq/doc/index.html) + all dependencies
  * [interproscan](https://www.ebi.ac.uk/interpro/)

The pipeline is designed and tested with Sun Grid Engine configured with a module load system.

## Installation
Use git to obtain a copy of the RSTrAP code

    git clone https://github.molgen.mpg.de/proost/RSTrAP

Next, move into the directory and copy **config.template.ini** and **data.template.ini**

    cd RSTrAP
    cp config.template.ini config.ini
    cp data.template.ini data.ini

Configure config.ini and data.ini using the guidelines below

## Configuration of RSTrAP
### config.ini
In your config file module names need to be specified. To see which modules are available on your system type:

    module avail

Add the module name for each of the tools to your config.ini, also update the paths to e.g. Trimmomatic.
In case the module load system isn't used, but all software is installed on the cluster + nodes set the modules to None !

Example config.ini:

```ini
[TOOLS]
; In case there is no module load system on the system set the module name to None

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

trimmomatic_se_command=java -jar /home/sepro/tools/Trimmomatic-0.36/trimmomatic-0.36.jar SE -threads 1  ${in} ${out}  ILLUMINACLIP:/home/sepro/tools/Trimmomatic-0.36/adapters/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
trimmomatic_pe_command=java -jar /home/sepro/tools/Trimmomatic-0.36/trimmomatic-0.36.jar PE -threads 1  ${ina} ${inb} ${outap} ${outau} ${outbp} ${outbu} ILLUMINACLIP:/home/sepro/tools/Trimmomatic-0.36/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36

tophat_se_cmd=tophat -o ${out} ${genome} ${fq}
tophat_pe_cmd=tophat -o ${out} ${genome} ${forward},${reverse}

samtools_cmd=samtools view -h -o ${out} ${bam}
htseq_count_cmd=htseq-count -s no -t ${feature} -i ${field} ${sam} ${gff} > ${out}

interproscan_cmd=interproscan.sh -i ${in_dir}/${in_prefix}${SGE_TASK_ID} -o ${out_dir}/${out_prefix}${SGE_TASK_ID} -f tsv -dp -iprlookup -goterms --tempdir /tmp

```

### data.ini
The location of your data needs to be defined in your data.ini file.

Example data.ini file:
```ini
[GLOBAL]
genomes=zma
email=None

[zma]
cds_fasta=/scratch/sepro/RSTrAP/data/zma/Zea_mays.AGPv3.22.cdna.clean.all.fa
genome_fasta=/scratch/sepro/RSTrAP/data/zma/Zea_mays.AGPv3.31.dna.genome.fa
gff_file=/scratch/sepro/RSTrAP/data/zma/zea_mays.protein_coding.gff
protein_fasta=/scratch/sepro/RSTrAP/data/zma/Zea_mays.AGPv3.22.pep.all.fa

gff_feature=CDS
gff_id=Parent

fastq_dir=/scratch/sepro/RSTrAP/data/zma/fastq_test

bowtie_output=/scratch/sepro/RSTrAP/output/bowtie/zma
trimmomatic_output=/scratch/sepro/RSTrAP/output/zma/trimmed
tophat_output=/scratch/sepro/RSTrAP/output/tophat/zma
samtools_output=/scratch/sepro/RSTrAP/output/samtools/zma
htseq_output=/scratch/sepro/RSTrAP/output/htseq/zma
exp_matrix_output=/scratch/sepro/RSTrAP/output/htseq/zma.expression.matrix.txt
exp_matrix_tpm_output=/scratch/sepro/RSTrAP/output/htseq/zma.expression.matrix.tpm.txt
exp_matrix_rpkm_output=/scratch/sepro/RSTrAP/output
interpro_output=/scratch/sepro/RSTrAP/output/interpro/zma
```

## Running RSTrAP
Once properly configured for your system and data, RSTrAP can be run using a single simple command

    ./run.py config.ini data.ini

Options to skip certain steps of the pipeline are included, use the command below for more info

    ./run.py -h

