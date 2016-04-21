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

### data.ini

## Running RSTrAP
Once properly configured for your system and data, RSTrAP can be run using a single simple command

    ./run.py config.ini data.ini

Options to skip certain steps of the pipeline are included, use the command below for more info

    ./run.py -h

