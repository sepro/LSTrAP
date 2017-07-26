#!/usr/bin/env python3
import argparse
import sys

from pipeline.check.sanity import check_sanity_config, check_sanity_data
from pipeline.interpro import InterProPipeline
from pipeline.transcriptome import TranscriptomePipeline
from pipeline.orthology import OrthologyPipeline


def run_pipeline(args):
    """
    Runs pipeline based on settings in args.

    :param args: Parsed arguments from argparse
    """
    if check_sanity_config(args.config) and check_sanity_data(args.data):
        if args.transcriptomics:
            tp = TranscriptomePipeline(args.config,
                                       args.data,
                                       enable_log=args.enable_log,
                                       use_hisat2=args.use_hisat2)

            if args.indexing:
                tp.prepare_genome()
            else:
                print("Skipping Indexing", file=sys.stderr)

            if args.trim_fastq:
                tp.trim_fastq()
            else:
                print("Skipping Trimmomatic", file=sys.stderr)

            if args.alignment:
                    tp.run_alignment(keep_previous=args.keep_intermediate)
            else:
                print("Skipping Alignment", file=sys.stderr)

            if args.htseq:
                tp.run_htseq_count(keep_previous=args.keep_intermediate)
            else:
                print("Skipping htseq-counts", file=sys.stderr)

            if args.qc:
                tp.check_quality()
            else:
                print("Skipping quality control", file=sys.stderr)

            if args.exp_matrix:
                tp.htseq_to_matrix()
                tp.normalize_rpkm()
                tp.normalize_tpm()
            else:
                print("Skipping expression matrix", file=sys.stderr)

            if args.pcc:
                tp.run_pcc()
            else:
                print("Skipping PCC calculations", file=sys.stderr)

            if args.mcl:
                tp.cluster_pcc()
            else:
                print("Skipping MCL clustering of PCC values", file=sys.stderr)
        else:
            print("Skipping transcriptomics", file=sys.stderr)

        # Run InterPro Section
        if args.interpro:
            ip = InterProPipeline(args.config, args.data)
            ip.run_interproscan()
        else:
            print("Skipping Interpro", file=sys.stderr)

        # Run Orthology Section
        if args.orthology:
            op = OrthologyPipeline(args.config, args.data)
            if args.orthofinder:
                op.run_orthofinder()

            if args.mcl_families:
                op.run_mcl()
        else:
            print("Skipping Orthology", file=sys.stderr)

    else:
        print("Sanity check failed, cannot start pipeline", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="./run.py")

    parser.add_argument('config', help='path to config.ini')
    parser.add_argument('data', help='path to data.ini')

    # Optional arguments
    parser.add_argument('--skip-transcriptomics', dest='transcriptomics', action='store_false', help='add --skip-transcriptomics to skip the entire transcriptome step')
    parser.add_argument('--enable-interpro', dest='interpro', action='store_true', help='Runs InterProScan to detect protein domains and provide functional annotation')
    parser.add_argument('--enable-orthology', dest='orthology', action='store_true', help='Runs OrhtoFinder and MCL to detect orthogroups, gene families and orthologs')

    parser.add_argument('--use-hisat2', dest='use_hisat2', action='store_true', help='Use HISAT2 to build the index and align reads instead of BowTie2 and TopHat2')

    parser.add_argument('--skip-indexing', dest='indexing', action='store_false', help='add --skip-indexing to skip building an index (for read alignment) on the genome (BowTie2 or HISAT2)')
    parser.add_argument('--skip-trim-fastq', dest='trim_fastq', action='store_false', help='add --skip-trim-fastq to skip trimming fastq files using trimmomatic')
    parser.add_argument('--skip-alignment', dest='alignment', action='store_false', help='add --skip-alignment to skip the read alignment step (TopHat 2 or HISAT2)')
    parser.add_argument('--skip-htseq', dest='htseq', action='store_false', help='add --skip-htseq to skip counting reads per gene with htseq-count')
    parser.add_argument('--skip-qc', dest='qc', action='store_false', help='add --skip-qc to skip quality control of tophat and htseq output')
    parser.add_argument('--skip-exp-matrix', dest='exp_matrix', action='store_false', help='add --skip-exp-matrix to skip converting htseq files to an expression matrix')
    parser.add_argument('--skip-pcc', dest='pcc', action='store_false', help='add --skip-pcc to skip calculating PCC values')
    parser.add_argument('--skip-mcl', dest='mcl', action='store_false', help='add --skip-mcl to skip clustering PCC values using MCL')

    parser.add_argument('--skip-orthofinder', dest='orthofinder', action='store_false', help='add --skip-orthofinder to skip the orthology detection')
    parser.add_argument('--skip-mcl-families', dest='mcl_families', action='store_false', help='add --skip-mcl to skip clustering blast with MCL')

    parser.add_argument('--remove-intermediate', dest='keep_intermediate', action='store_false', help='add --remove-intermediate to clear trimmomatic and tophat files after completing those steps')
    parser.add_argument('--disable-log', dest='enable_log', action='store_false',
                        help='add --disable-log to disable writing additional statistics.')

    # Flags for the big sections of the pipeline
    parser.set_defaults(transcriptomics=True)
    parser.set_defaults(interpro=False)
    parser.set_defaults(orthology=False)

    parser.set_defaults(use_hisat2=False)

    # Flags for individual tools for transcriptomics
    parser.set_defaults(indexing=True)
    parser.set_defaults(trim_fastq=True)
    parser.set_defaults(alignment=True)
    parser.set_defaults(htseq=True)
    parser.set_defaults(qc=True)
    parser.set_defaults(exp_matrix=True)
    parser.set_defaults(pcc=True)
    parser.set_defaults(mcl=True)

    parser.set_defaults(orthofinder=True)
    parser.set_defaults(mcl_families=True)

    parser.set_defaults(keep_intermediate=True)
    parser.set_defaults(enable_log=True)

    # Parse arguments and start pipeline
    args = parser.parse_args()

    run_pipeline(args)
