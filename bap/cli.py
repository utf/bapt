# coding: utf-8
# Copyright (c) Alex Ganose
# Distributed under the terms of the MIT License.

import os
import argparse

from bap import read_config
from bap.plotter import BandAlignmentPlotter

__author__ = "Alex Ganose"
__version__ = "0.1"
__maintainer__ = "Alex Ganose"
__email__ = "alexganose@googlemail.com"
__date__ = "Oct 19, 2017"


def bap(band_edge_data, output='alignment.pdf'):
    baper = BandAlignmentPlotter(band_edge_data)
    plt = baper.get_plot()
    plt.savefig(output)


def main():
    parser = argparse.ArgumentParser(description="""
    Plotter for electronic band alignment diagrams.""",
                                     epilog="""
    Author: {}
    Version: {}
    Last updated: {}""".format(__author__, __version__, __date__))
    parser.add_argument('-f', '--filename', default=None,
                        help='Path to file containing alignment information.')
    parser.add_argument('-n', '--name',
                        help='List of compound names (comma seperated).' +
                        'Must be used in conguction with --ip and --ea.')
    parser.add_argument('-i', '--ip',
                        help='List of ionisation potentials (comma separated).')
    parser.add_argument('-e', '--ea',
                        help='List of electron affinities (comma separated).')
    parser.add_argument('-o', '--output', default='alignment.pdf',
                        help='Output file name (defaults to alignment.pdf).')
    args = parser.parse_args()

    emsg = None
    if not args.filename and not (args.name or args.ip or args.ea):
        emsg = "ERROR: no arguments specified."
    elif not args.filename and not (args.name and args.ip and args.ea):
        emsg = "ERROR: --name, --ip and --ea flags must specified concurrently."
    elif args.filename and (args.name or args.ip or args.ea):
        emsg = "ERROR: filename and name/ip/ea specified simulatenously."

    if emsg:
        print(emsg)
        os.exit()

    if args.filename:
        data = read_config(args.filename)
    else:
        data = [{'name': name, 'ip': ip, 'ea': ea} for name, ip, ea in
                zip(args.name, args.ip, args.ea)]
    bap(data, output=args.output)

if __name__ == "__main__":
    main()
