# Preparing your system

LSTrAP is designed to run on the head node of a Oracle Grid Engine cluster. Apart from a running compute cluster, the essential 
tools need to be installed. A full list is provided below, tools can be installed on the grid nodes directly or inside modules. 
When opting for the latter, the configuration file needs to contain the exact names of the modules containing the tools.


  * [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)
  * [tophat](https://ccb.jhu.edu/software/tophat/manual.shtml)
  * [samtools](http://www.htslib.org/)
  * [sratools](http://ncbi.github.io/sra-tools/)
  * [python 2.7](https://www.python.org/download/releases/2.7/) + [HTSeq](http://www-huber.embl.de/users/anders/HTSeq/doc/index.html) + all dependencies (including [PySam](https://github.com/pysam-developers/pysam))
  * [python 3.5](https://www.python.org/download/releases/3.5.1/) + SciPy + [Numpy](http://www.numpy.org/)
  * [interproscan](https://www.ebi.ac.uk/interpro/)
  * [OrthoFinder](https://github.com/davidemms/OrthoFinder)
  * [MCL](http://www.micans.org/mcl/index.html?sec_software)
  * [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic)