#!/usr/bin/env python3

from sys import argv
from time import sleep
from monitor import Monitor

def parse_args(args):
    options = {
        '-t': 'temp',
        '-c': 'usage',
        '-p': 'power'
    }
    return tuple(options[arg] for arg in args)

def main():
    options = parse_args(argv[1:])
    monitor = Monitor(options)

    print(*options, sep=',')

    try:
        while True:
            sample = monitor.all()
            print(*(sample[op] for op in options), sep=',')
            sleep(0.2)

    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__': main()
