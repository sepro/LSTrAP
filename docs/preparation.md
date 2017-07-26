# Preparing your system

LSTrAP is designed with High Performance Computing in mind and requires a computer cluster running 
[Oracle Grid Engine]((https://www.oracle.com/sun/index.html)) or [PBS](https://en.wikipedia.org/wiki/Portable_Batch_System) 
/ [Torque](http://www.adaptivecomputing.com/products/open-source/torque/). Furthermore, the essential 
tools (see below) need to be installed prior to running LSTrAP. 
Using the [Environment modules](http://modules.sourceforge.net/) are supported, in that case the configuration file 
needs to contain the exact names of the modules containing the tools.

## Required Tools

  * [Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)
  * [TopHat](https://ccb.jhu.edu/software/tophat/manual.shtml)
  * [HISAT2](http://ccb.jhu.edu/software/hisat2/index.shtml)
  * [Samtools](http://www.htslib.org/)
  * [SRAtools](http://ncbi.github.io/sra-tools/)
  * [HTSeq](http://www-huber.embl.de/users/anders/HTSeq/doc/index.html) + all dependencies (including [PySam](https://github.com/pysam-developers/pysam))
  * [Python 3.5](https://www.python.org/download/releases/3.5.1/) + SciPy + [Numpy](http://www.numpy.org/)
  * [MCL](http://www.micans.org/mcl/index.html?sec_software)
  * [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic)
  
## Optional tools

  * [InterProScan](https://www.ebi.ac.uk/interpro/)
  * [OrthoFinder](https://github.com/davidemms/OrthoFinder)
  * [Python 2.7](https://www.python.org/download/releases/2.7/) (for OrthoFinder)
  * [scikit-learn](http://scikit-learn.org/) for Python 3, required for PCA analysis (helper script)
  * [seaborn](https://stanford.edu/~mwaskom/software/seaborn/) for Python 3, required for PCA analysis (helper script)
  * [Aspera connect client](http://downloads.asperasoft.com/en/downloads/2), required for the *get_sra_ip.py* (helper script)