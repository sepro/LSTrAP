#!/usr/bin/env python3
import argparse
import sys

from pipeline.transcriptome import TranscriptomePipeline
from pipeline.sanity import check_sanity_config, check_sanity_data


def run_pipeline(args):
    """
    Runs pipeline based on settings in args.

    :param args: Parsed arguments from argparse
    """
    if check_sanity_config(args.config) and check_sanity_data(args.data):
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
    else:
        print("Sanity check failed, cannot start pipeline", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="./run.py")

    parser.add_argument('config', help='path to config.ini')
    parser.add_argument('data', help='path to data.ini')

    # Optional arguments
    parser.add_argument('--skip-bowtie-build', dest='bowtie_build', action='store_false', help='add --skip-bowtie-build to skip the step that indexes the genomes using bowtie-build')
    parser.add_argument('--skip-trim-fastq', dest='trim_fastq', action='store_false', help='add --skip-trim-fastq to skip trimming fastq files using trimmomatic')
    parser.add_argument('--skip-tophat', dest='tophat', action='store_false', help='add --skip-tophat to skip read mapping with tophat')

    parser.set_defaults(bowtie_build=True)
    parser.set_defaults(trim_fastq=True)
    parser.set_defaults(tophat=True)

    # Parse arguments and start pipeline
    args = parser.parse_args()

    run_pipeline(args)
