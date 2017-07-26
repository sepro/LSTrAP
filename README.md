# LSTrAP

LSTrAP, short for Large Scale Transcriptome Analysis Pipeline, greatly facilitates the construction of co-expression networks from
RNA-Seq data. The various tools involved are seamlessly connected and  CPU-intensive steps are submitted to a computer cluster 
automatically. 

## Version 1.3 Changelog

  * Support for [PBS](https://en.wikipedia.org/wiki/Portable_Batch_System) / [Torque](http://www.adaptivecomputing.com/products/open-source/torque/) scheduler (note proper [configuration](./docs/configuration.md) is required)
  * [HISAT2](https://ccb.jhu.edu/software/hisat2/index.shtml) can be used as an alternative to [BowTie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml) and [TopHat 2](https://ccb.jhu.edu/software/tophat/index.shtml)
  * Added [helper](./docs/helper.md) script to do PCA on samples
  * **Parameter names in data.ini changed, additional options added to config.ini**. Check the [configuration](./docs/configuration.md)
   and update the files accordingly.

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

## Further reading

  * [LSTrAP output](docs/example_output.md)
  * [Quality statistics](docs/quality.md): How to check the quality of samples and remove problematic samples
  * [Helper Scripts](docs/helper.md): To acquire data from the [Sequence Read Archive](https://www.ncbi.nlm.nih.gov/sra)
  and process results.

    
## Contact

LSTrAP was developed by [Sebastian Proost](mailto:proost@mpimp-golm.mpg.de) and [Marek Mutwil](mailto:mutwil@gmail.com) at the [Max-Planck Institute for Molecular Plant Physiology](http://www.mpimp-golm.mpg.de/2168/en)

## Acknowledgements and Funding

This work is supported by [ERA-CAPS](http://www.eracaps.org/) though the [EVOREPRO](http://www.evorepro.org/) project. 
The authors would like to thank Andreas Donath for technical support and helpful discussions.

## License

LSTrAP is freely available under the [MIT License](LICENSE.md)
