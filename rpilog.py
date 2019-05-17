#!/usr/bin/env python3

from sys import argv
from time import sleep, time
from monitor import Monitor

def parse_args(args):
    options = {
        '-t': 'temp',
        '-c': 'usage',
        '-p': 'power'
    }
    options = (*filter(lambda arg: arg is not None, (options.get(arg) for arg in args)),)
    logfilename = args[-1] if args and args[-1][0] != '-' else None
    return options, logfilename

def main():
    options, logfilename = parse_args(argv[1:])
    monitor = Monitor(options)
    options = monitor.options

    logfile = None

    if logfilename:
        logfile = open(logfilename, 'w')
        output = lambda values: logfile.write(','.join(map(str, values)) + '\n')
    else:
        output = lambda values: print(*values, sep=',')

    output(('timestamp', *options))

    try:
        while True:
            sample = monitor.all()
            output((time(), *(sample[op] for op in options)))
            sleep(0.2)

    except KeyboardInterrupt:
        if logfile: logfile.close()
        exit(0)
        
if __name__ == '__main__': main()
