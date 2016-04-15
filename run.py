#!/usr/bin/env python3
import argparse

from pipeline.transcriptome import TranscriptomePipeline


def run_pipeline(config, data):
    tp = TranscriptomePipeline(config, data)

    tp.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="./run.py")
    parser.add_argument('config', help='path to config.ini')
    parser.add_argument('data', help='path to data.ini')

    args = parser.parse_args()

    run_pipeline(args.config, args.data)
