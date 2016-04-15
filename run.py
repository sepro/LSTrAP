import argparse


def run_pipeline(config, data):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="./run.py")
    parser.add_argument('config', help='path to config.ini')
    parser.add_argument('data', help='path to data.ini')

    run_pipeline(parser.config, parser.data)
