#!/usr/bin/env python

def obtain_options() -> argparse.Namespace
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', default='/tmp', help='Which Directory?')
    return parser.parse_args()

def run_factory():
    options = obtain_options()

if __name__ == '__main__':
    run_factory()
