#!/usr/bin/env python3
import argparse
import sys

from pipeline.transcriptome import TranscriptomePipeline


def run_pipeline(args):
    """
    Runs pipeline based on settings in args.

    :param args: Parsed arguments from argparse
    """
    tp = TranscriptomePipeline(args.config, args.data)

    if args.bowtie_build:
        tp.prepare_genome()
    else:
        print("Skipping Bowtie-build", file=sys.stderr)

    if args.trim_fastq:
        tp.trim_fastq()
    else:
        print("Skipping Trimmomatic", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="./run.py")

    parser.add_argument('config', help='path to config.ini')
    parser.add_argument('data', help='path to data.ini')

    # Optional arguments
    parser.add_argument('--skip-bowtie-build', dest='bowtie_build', action='store_false', help='add --skip-bowtie-build to skip the step that indexes the genomes using bowtie-build')
    parser.add_argument('--skip-trim-fastq', dest='trim_fastq', action='store_false', help='add --skip-trim-fastq to skip trimming fastq files using trimmomatic')

    parser.set_defaults(bowtie_build=True)
    parser.set_defaults(trim_fastq=True)

    # Parse arguments and start pipeline
    args = parser.parse_args()

    run_pipeline(args)
