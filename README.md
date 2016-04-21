# RSTrAP
Rna Seq Transcriptome Analysis Pipeline

## Requirements


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

