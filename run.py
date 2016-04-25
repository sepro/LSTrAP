#!/usr/bin/env python3
import argparse
import sys

from pipeline.check.sanity import check_sanity_config, check_sanity_data
from pipeline.interpro import InterProPipeline
from pipeline.transcriptome import TranscriptomePipeline


def run_pipeline(args):
    """
    Runs pipeline based on settings in args.

    :param args: Parsed arguments from argparse
    """
    if check_sanity_config(args.config) and check_sanity_data(args.data):
        if args.transcriptomics:
            tp = TranscriptomePipeline(args.config, args.data)

            if args.bowtie_build:
                tp.prepare_genome()
            else:
                print("Skipping Bowtie-build", file=sys.stderr)

            if args.trim_fastq:
                tp.trim_fastq()
            else:
                print("Skipping Trimmomatic", file=sys.stderr)

            if args.tophat:
                tp.run_tophat()
            else:
                print("Skipping Tophat", file=sys.stderr)

            if args.samtools:
                tp.run_samtools()
            else:
                print("Skipping Samtools", file=sys.stderr)

            if args.htseq:
                tp.run_htseq_count()
            else:
                print("Skipping htseq-counts", file=sys.stderr)

            if args.exp_matrix:
                tp.htseq_to_matrix()
            else:
                print("Skipping expression matrix", file=sys.stderr)
        else:
            print("Skipping transcriptomics", file=sys.stderr)

        if args.interpro:
            ip = InterProPipeline(args.config, args.data)
            ip.run_interproscan()
        else:
            print("Skipping Interpro", file=sys.stderr)

    else:
        print("Sanity check failed, cannot start pipeline", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="./run.py")

    parser.add_argument('config', help='path to config.ini')
    parser.add_argument('data', help='path to data.ini')

    # Optional arguments
    parser.add_argument('--skip-transcriptomics', dest='transcriptomics', action='store_false', help='add --skip-transcriptomics to skip the entire transcriptome step')

    parser.add_argument('--skip-bowtie-build', dest='bowtie_build', action='store_false', help='add --skip-bowtie-build to skip the step that indexes the genomes using bowtie-build')
    parser.add_argument('--skip-trim-fastq', dest='trim_fastq', action='store_false', help='add --skip-trim-fastq to skip trimming fastq files using trimmomatic')
    parser.add_argument('--skip-tophat', dest='tophat', action='store_false', help='add --skip-tophat to skip read mapping with tophat')
    parser.add_argument('--skip-samtools', dest='samtools', action='store_false', help='add --skip-samtools to skip bam to sam conversion using samtools')
    parser.add_argument('--skip-htseq', dest='htseq', action='store_false', help='add --skip-htseq to skip counting reads per gene with htseq-count')
    parser.add_argument('--skip-exp-matrix', dest='exp_matrix', action='store_false', help='add --skip-exp-matrix to skip converting htseq files to an expression matrix')

    parser.add_argument('--skip-interpro', dest='interpro', action='store_false', help='add --skip-interpro to skip the entire interproscan step')

    parser.set_defaults(transcriptomics=True)

    parser.set_defaults(bowtie_build=True)
    parser.set_defaults(trim_fastq=True)
    parser.set_defaults(tophat=True)
    parser.set_defaults(samtools=True)
    parser.set_defaults(htseq=True)
    parser.set_defaults(exp_matrix=True)

    parser.set_defaults(interpro=True)

    # Parse arguments and start pipeline
    args = parser.parse_args()

    run_pipeline(args)
