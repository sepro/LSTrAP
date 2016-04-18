#!/usr/bin/env python3
import argparse

from pipeline.transcriptome import TranscriptomePipeline


def run_pipeline(args):
    tp = TranscriptomePipeline(args.config, args.data)

    if args.bowtie_build:
        tp.prepare_genome()
    else:
        print("Skipping Bowtie-build")

    tp.process_fastq()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="./run.py")
    parser.add_argument('config', help='path to config.ini')
    parser.add_argument('data', help='path to data.ini')

    parser.add_argument('--skip-bowtie-build', dest='bowtie_build', action='store_false')
    parser.set_defaults(bowtie_build=True)

    args = parser.parse_args()

    run_pipeline(args)
