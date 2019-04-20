#!/usr/bin/env python3

from sys import argv
from time import sleep
from monitor import Monitor

def main():
    monitor = Monitor(argv[1:])

    while True:
        print(monitor.all())
        sleep(1)

if __name__ == '__main__': main()
