#!/usr/bin/env python3

from sys import argv
from time import sleep
from monitor import Monitor

def parse_args(args):
    opt_table = {
        '-h': 'help',
        '-t': ('temp',),
        '-c': ('usage',),
        '-p': ('power',),
        '-m': ('ram',),
        '-n': ('net_down', 'net_up'),

        '--help':     ('help',),
        '--temp':     ('temp',),
        '--cpu':      ('usage',),
        '--power':    ('power',),
        '--mem':      ('ram',),
        '--net_down': ('net_down',),
        '--net_up':   ('net_up',),
    }

    options = tuple(opt
        for opt_t in filter(lambda arg: arg is not None, (opt_table.get(arg) for arg in args))
        for opt in opt_t)
    logfilename = args[-1] if args and args[-1][0] != '-' else None
    return options, logfilename

def show_help():
    help_str = """
    NAME
            rpilog - show info on Rasbperry Pi

    SYNOPSIS
            rpilog [OPTIONS]
            rpilog [OPTIONS] FILE

    OPTIONS
            -h, --help
                    show help

            -t, --temp
                    log CPU temperature

            -c, --cpu
                    log CPU usage

            -p, --power
                    log Raspberry Pi power comsumption

            -m, --mem
                    log RAM usage

            --net_down
                    log download rate

            --net_up
                    log upload rate

            -n, --net
                    log both download and upload rates
    """

    print(help_str); exit(0)

def main():
    options, logfilename = parse_args(argv[1:])

    if 'help' in options: show_help()

    monitor = Monitor(options)
    options = ('timestamp', *sorted(monitor.options))

    logfile = None

    if logfilename:
        logfile = open(logfilename, 'w')
        output = lambda values: logfile.write(','.join(map(str, values)) + '\n')
    else:
        output = lambda values: print(*values, sep=',')

    output(options)

    try:
        while True:
            sample = monitor.all()
            output(sample[op] for op in options)
            sleep(0.2)

    except KeyboardInterrupt:
        if logfile: logfile.close()
        exit(0)

if __name__ == '__main__': main()
