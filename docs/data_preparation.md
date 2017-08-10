# Preparing your data

LSTrAP has a few expectations to the way RNASeq files are pre-processed. When using the [included scripts](helper.md) 
to download samples from the Sequence Read Archive and converting them to (compressed) .fastq files this is done 
automatically. When including your own data some pre-processing might be required, read the suggestions below how to get
other data ready for processing using LSTrAP.

## Preparing RNA-Seq data

RNA-Seq data needs to be **de-multiplexed** and in **.fastq format** prior to running LSTrAP. 
For single-end samples you need one file (output needs to be merged) for paired-end reads you need to files which have 
the same  filename except for a suffix, _1 for the left reads, _2 for the right (e.g. paired_end_sample_1.fastq.gz and 
paired_end_sample_2.fastq.gz).

The extension should be .fq or .fastq for uncompressed files, .fq.gz and .fastq.gz for compressed files (only gzip is
supported).

### Merging files

Samples are commonly split and sequenced in different lanes or runs (to increase the total number of reads), those files
need to be combined prior to starting LSTrAP. Fastq file can be done using default linux commands. Pay attention when 
merging paired-end files.

    # Merge two single-end samples, compressed with gzip
    zcat sample_one_part_1.fastq.gz sample_one_part_2.fastq.gz | gzip -c > sample_one_merged.fastq.gz
     
    # Merge two uncompressed, single-end files
    cat sample_one_part_1.fastq sample_one_part_2.fastq > sample_one_merged.fastq
        
    # Merge two uncompressed, single-end files and compress the result
    cat sample_one_part_1.fastq sample_one_part_2.fastq | gzip -c > sample_one_merged.fastq.gz
     
    # Merge paired-end files
    zcat sample_one_L001_R1.fastq.gz sample_one_L002_R1.fastq.gz | gzip -c > sample_one_merged_1.fastq.gz
    zcat sample_one_L001_R2.fastq.gz sample_one_L002_R2.fastq.gz | gzip -c > sample_one_merged_2.fastq.gz
    
**Note**: In theory, gzipped files can be concatenated directly, which is much more efficiently than using zcat paired with 
gzip. However this might lead to [errors](https://www.biostars.org/p/81924/#82017) with some tools, use this method 
carefully at your **own risk**.

    # Merge two single-end samples, compressed with gzip
    cat sample_one_part_1.fastq.gz sample_one_part_2.fastq.gz > sample_one_merged.fastq.gz
     
    # Merge paired-end files
    cat sample_one_L001_R1.fastq.gz sample_one_L002_R1.fastq.gz > sample_one_merged_1.fastq.gz
    cat sample_one_L001_R2.fastq.gz sample_one_L002_R2.fastq.gz > sample_one_merged_2.fastq.gz   

### Converting files to Fastq

If you have files in .sam/.bam or .sra format, these need to be converted to .fastq or .fastq.gz files. 
[Samtools](http://www.htslib.org/doc/samtools.html) allows conversion from .sam/.bam to .fastq while 
[SraToolKit](https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=software) included fastq-dump to convert .sra files.

For converting .sra files a [helper script](helper.md) is included.

    # SAMTools
    samtools fastq input.bam > output.fastq
    samtools fastq input.bam | gzip -c > output.fastq.gz
     
    # SRAToolKit
    fastq-dump --gzip --skip-technical --readids --dumpbase --split-3 input.sra -O output_dir/
    

### De-multiplexing files

In some cases the sequences might not be de-multiplexed by the sequencing facility, for de-multiplexing RNA-Seq files a 
third-party tool is required.  

  * [fastq-multx](https://github.com/ExpressionAnalysis/ea-utils/blob/wiki/FastqMultx.md)
  * [REAPER](http://wwwdev.ebi.ac.uk/enright-dev/kraken/reaper/src/reaper-latest/doc/reaper.html)
  
  
## Recommended folder structure (optional)

When using LSTrAP keeping a consistent file/folder structure for input and output (as specified in data.ini) is 
recommended. This allows data.ini to be quickly adopted for novel projects.

Below if the structure we've adopted for our projects.

```
./
|-- config.ini
|-- data.ini
+-- data/
    +-- fastq/
        |-- sample_one.fastq.gz
        |-- paired_end_S01_1.fastq.gz
        |-- paired_end_S01_2.fastq.gz
        +-- ...
    +-- genome/
        |-- species.genome.fasta
        |-- species.cds.fasta
        |-- species.pep.fasta
        +-- species.genes.gff
+-- output
    +-- species
        |-- index_files
        +-- alignment_tophat/
            |-- sample_one/
            |-- paired_end_S01/
            +-- ...
        +-- htseq/
            |-- sample_one.htseq
            |-- paired_end_S01.htseq
            +-- ...
        +-- expression/
            |-- matrix.raw.txt
            |-- matrix.tpm.txt
            |-- matrix.rpkm.txt
            |-- pcc.table.txt
            |-- pcc.mcl.txt
            +-- mcl.clusters.txt
```



