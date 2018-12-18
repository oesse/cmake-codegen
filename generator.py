#!/usr/bin/env python3
import argparse
import sys

def read_interface_names(ifile):
    with open(ifile) as f:
        return [line.strip('\n') for line in f.readlines() if line != '\n']


def generate_header(name):
    lines = ['#pragma once',
             'struct {} {{ const char *name(); }};'.format(name)]
    write_lines('{}.hpp'.format(name), lines)


def generate_implementation(name):
    lines = ['#include "{}.hpp"'.format(name),
             'const char *{0}::name(){{ return "Hello from {0}!"; }};'.format(name)]
    write_lines('{}.cpp'.format(name), lines)


def write_lines(filename, lines):
    with open(filename, 'w') as f:
        for l in lines:
            f.write(l + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate some cpp/hpp files.')
    parser.add_argument('inputfile')
    parser.add_argument('--print-dependencies',
                        dest='print_dependencies',
                        action='store_const',
                        default=False,
                        const=True,
                        help='Print file dependencies, do not generate anything')
    args = parser.parse_args()

    interfaces = read_interface_names(args.inputfile)
    if args.print_dependencies:
        sep = ';'
        print(sep.join(['{0}.hpp{1}{0}.cpp'.format(name, sep) for name in interfaces]), end='')
        sys.exit(0)

    for interface in interfaces:
        generate_header(interface)
        generate_implementation(interface)
