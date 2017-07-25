# LSTrAP

LSTrAP, short for Large Scale Transcriptome Analysis Pipeline, greatly facilitates the construction of co-expression networks from
RNA-Seq data. The various tools involved are seamlessly connected and  CPU-intensive steps are submitted to a computer cluster 
automatically. 

## Version 1.3 Changelog

  * Support for [PBS](https://en.wikipedia.org/wiki/Portable_Batch_System) / [Torque](http://www.adaptivecomputing.com/products/open-source/torque/) scheduler (note proper [configuration](./docs/configuration.md) is required)
  * [HISAT2](https://ccb.jhu.edu/software/hisat2/index.shtml) can be used as an alternative to [BowTie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml) and [TopHat 2](https://ccb.jhu.edu/software/tophat/index.shtml)
  * Added [helper](./docs/helper.md) script to do PCA on samples
  * **Parameter names in data.ini changed**

## Workflow

LSTrAP wraps multiple existing tools into a single workflow. To use LSTrAP the following tools need to be installed

![LSTrAP Workflow](docs/images/LSTrAP_workflow.png "Steps automated by LSTrAP")

Steps in bold are submitted to a cluster. Optional steps can be enabled by adding the flag *&#8209;&#8209;enable&#8209;interpro* and/or 
*&#8209;&#8209;enable&#8209;orthology*.

## Installation
Before installing make sure your system meets all requirements. A detailed list of supported systems and required 
software can be found [here](docs/preparation.md).


Use git to obtain a copy of the LSTrAP code

    git clone https://github.molgen.mpg.de/proost/LSTrAP

Next, move into the directory and copy **config.template.ini** and **data.template.ini**

    cd LSTrAP
    cp config.template.ini config.ini
    cp data.template.ini data.ini

Configure config.ini and data.ini using these [guidelines](docs/configuration.md)


## Running LSTrAP

Once properly configured for your system and data, LSTrAP can be run using a single simple command (that should be 
executed on the head node).

    ./run.py config.ini data.ini

Run using [HISAT2](https://ccb.jhu.edu/software/hisat2/index.shtml)

    ./run.py --use-hisat2 config.ini data.ini

Run with InterProScan and/or OrthoFinder 

    ./run.py --enable-orthology --enable-interproscan config.ini data.ini

Furthermore, steps can be skipped (to avoid re-running steps unnecessarily). Use the command below for more info.

    ./run.py -h

## Obtaining and preparing data

Scripts to download and prepare data from the [Sequence Read Archive](https://www.ncbi.nlm.nih.gov/sra) are included in
LSTrAP in the folder **helper**. Furthermore, it is recommended to remove splice variants from the GFF3 files, a script
to do that is included there as well. Detailed instructions for each script provided to obtain and prepare data can be
found [here](docs/helper.md)

## Quality report

After running LSTrAP a log file (*lstrap.log*) is written, in which samples which failed a quality measure
are reported. Note that __no samples are excluded from the final network__. In case certain samples need to be excluded
from the final network remove the htseq file for the sample you which to exclude and re-run the pipeline skipping all
steps prior to building the network.

    ./run.py config.ini data.ini --skip-interpro --skip-orthology --skip-bowtie-build --skip-trim-fastq --skip-tophat --skip-htseq --skip-qc

More information on how the quality of samples is determined can be found [here](docs/quality.md).

## Output

Apart from the output all tools included generate, LSTrAP will generate raw and normalized expression matrices, a 
co&#8209;expression network and co&#8209;expression clusters.

A detailed overview of files produces, including examples, can be found [here](docs/example_output.md).

## Helper Scripts

LSTrAP comes with a few additional scripts to assist users to download and process data from the [Sequence Read Archive](http://www.ncbi.nlm.nih.gov/sra),
repeat analyses and the case study reported in the manuscript (Proost et al., *under preparation*).

Details for each script can be found [here](docs/helper.md)

## Running LSTrAP on transcriptome data

To use LSTrAP on a *de novo* assembled transcriptome a little pre-processing is required. Instead of the genome a fasta 
file containing **coding** sequences can be used (remove UTRs). Using the helper script fasta_to_gff.py a gff file suited
for LSTrAP can be generated.

    python3 fasta_to_gff.py /path/to/transcript.cds.fasta > output.gff
    
 
    
## Contact

LSTrAP was developed by [Sebastian Proost](mailto:proost@mpimp-golm.mpg.de) and [Marek Mutwil](mailto:mutwil@mpimp-golm.mpg.de) at the [Max-Planck Institute for Molecular Plant Physiology](http://www.mpimp-golm.mpg.de/2168/en)

## Acknowledgements and Funding

This work is supported by [ERA-CAPS](http://www.eracaps.org/) though the [EVOREPRO](http://www.evorepro.org/) project. 
The authors would like to thank Andreas Donath for technical support and helpful discussions.

## License

LSTrAP is freely available under the [MIT License](LICENSE.md)
