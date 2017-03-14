# Example output

Upon completion, LSTrAP will have run Trimmomatic, Bowtie 2, TopHat2 and HTSeq-Count. Unless specified otherwise, the 
raw output from those tools will be stored. Furthermore, LSTrAP further processes the output of these tools to construct
expression matrices, co-expression networks and clusters. A description of the LSTrAP specific output can be found 
below.

## Expression profiles/matrix

LSTrAP will write the raw expression matrix as well as an RPKM and TPM normalized version upon completion. This is a 
large matrix where columns (separated by tabs) are samples and rows are transcripts. In each cell the raw or normalized expression value 
is included. Mock example is included below.

A single row, along with the header, can be used to draw an expression profile (cfr. in Excel, R, ...)

    gene    Sample1 Sample2 Sample3 ... Sample10
    Gene1   2       1       3       ... 0
    Gene2   0       0.5     0       ... 0
    Gene3   2       0.22    0.11    ... 0.5
    ...     ...     ...     ...     ... ...
    Gene10  1       3       0       ... 0.7            
    
## Co-expression network

Pearson's Correlation Coefficients (PCC) are calculated based on the TPM normalized expression matrix. A file is written
where for each transcript (ID before the colon) the top 1000 co-expressed genes (ID after colon, tab separated) are shown with the PCC value 
(number between round brackets).

    AT1G05660.1: AT1G06120.1(0.975109345421)        AT4G01630.1(0.971643917372)     AT3G59130.1(0.967450941397)     AT2G39040.1(0.961912892051)     AT2G43880.1(0.958996761442) ...
    AT5G09780.1: AT3G17010.1(0.949034133987)        AT5G57720.1(0.870169887662)     AT2G16210.1(0.8604233184)       AT5G47600.1(0.818799585331)     AT5G37860.1(0.801435539475) ...
    AT2G19740.1: AT3G02560.1(0.842648087998)        AT5G28060.1(0.837579535602)     AT5G56710.1(0.835775366218)     AT2G44860.1(0.828341737973)     AT2G39460.1(0.828069004117) ...
    ...
    
Furthermore, the co-expression network is prepared for MCL clustering. Here only co-expressed pairs with PCC 
values > 0.7 are considered. The score stored in this file is PCC - 0.7 as MCL requires the minimal value to be zero.
On each line you have two co-expressed genes and the correlation transformed for use with mcl. This file can be imported
into Cytoscape desktop or Gephi for visualization/further analysis. 

    AT1G67450.1     AT4G23110.1     0.0496500079172
    AT1G67450.1     AT4G05630.1     0.0490984038043
    AT1G67450.1     AT5G40430.1     0.0479090219126
    ...
    
# Co-expression clusters

Co-expression clusters, detected using MCL, are stored as a text file where each line represents a co-expression 
cluster. IDs for transcripts belonging to that cluster are separated by tabs. 

    AT2G19740.1     AT3G02560.1     AT5G28060.1     AT5G56710.1     AT2G44860.1     AT2G39460.1     AT1G34030.1     AT1G26880.1     AT3G28900.1     AT3G04920.1 ...
    AT1G69250.1     AT1G52640.1     AT5G15820.1     AT1G17130.1     AT3G24210.1     AT5G27330.1     AT4G21140.1     AT4G12610.1     AT5G49000.1     AT4G25340.1 ...
    AT1G27500.1     AT1G04700.1     AT3G24715.1     AT3G57140.1     AT4G07960.1     AT2G30505.1     AT1G79860.1     AT1G44120.1     AT1G05820.1     AT1G52240.1 ...
    AT2G40030.1     AT3G51290.1     AT4G39600.1     AT2G02790.1     AT3G07200.1     AT2G27040.1     AT5G14610.1     AT3G17840.1     AT2G39620.1     AT2G40720.1 ...
    AT5G05657.1     AT2G16881.1     AT3G23650.1     AT4G23103.1     AT4G08370.1     AT3G24216.1     AT2G02280.1     AT3G31068.1     AT2G01780.1     AT2G03932.1 ...
    AT1G32520.1     AT4G09350.1     AT1G62250.1     AT3G47430.1     AT2G37240.1     AT2G04039.1     AT2G35660.1     AT5G09660.1     AT2G39730.1     AT4G26860.1 ...
    ...