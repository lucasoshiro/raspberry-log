#!/usr/bin/env python3

from sys import argv
from time import sleep
from monitor import Monitor

opt_table = [
    ('h',  'help',     ('help',),              'show help'),
    ('t',  'temp',     ('temp',),              'log CPU temperature'),
    ('c',  'cpu',      ('usage',),             'log CPU usage'),
    ('p',  'power',    ('power',),             'log Raspberry Pi power comsumption'),
    ('m',  'mem',      ('ram',),               'log RAM usage'),
    (None, 'net_down', ('net_down',),          'log download rate'),
    (None, 'net_up',   ('net_up',),            'log upload rate'),
    ('n',  None,       ('net_down', 'net_up'), 'log both download and upload rates'),
]              

def parse_args(args):
    flags = [*filter(lambda arg: arg[0] == '-', args)]

    simple = filter(lambda flag: len(flag) >= 2 and flag[1] != '-', flags)
    simple = list(''.join(x[1:] for x in simple))

    double = filter(lambda flag: len(flag) >= 3 and flag[1] == '-', flags)
    double = [x[2:] for x in double]

    
    logfilename = args[-1] if args and args[-1][0] != '-' else None

    simple_opt = {flag: opt for flag, _, opt, __ in opt_table}
    double_opt = {flag: opt for _, flag, opt, __ in opt_table}

    options = [
        *(simple_opt[flag] for flag in simple),
        *(double_opt[flag] for flag in double)
    ]

    options = [e for t in options for e in t]

    return options, logfilename

def show_help():
    help_str = """
    NAME
            rpilog - show info on Rasbperry Pi

    SYNOPSIS
            rpilog [OPTIONS]
            rpilog [OPTIONS] FILE

    OPTIONS
{}
    """

    opt_str = """
           {}
                   {}
"""

    print(help_str.format(
        '\n'.join(
            opt_str.format(
                ('-{} '.format(opt[0]) if opt[0] else '') +
                ('--{}'.format(opt[1]) if opt[1] else ''),
                opt[3])
            for opt in opt_table
        )))
    exit(0)

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
