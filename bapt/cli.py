# coding: utf-8
# Copyright (c) Alex Ganose
# Distributed under the terms of the MIT License.

import sys
import argparse

from bapt import read_config, get_plot

__author__ = "Alex Ganose"
__version__ = "0.1"
__maintainer__ = "Alex Ganose"
__email__ = "alexganose@googlemail.com"
__date__ = "Oct 19, 2017"


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
    parser.add_argument('--show-ea', action='store_true', dest='show_ea',
                        help='Display the electron affinity value.')
    parser.add_argument('--show-axis', action='store_true', dest='show_axis',
                        help='Display the energy yaxis bar and label.')
    parser.add_argument('--height', type=float, default=5,
                        help='Set figure height in inches.')
    parser.add_argument('--width', type=float, default=None,
                        help='Set figure width in inches.')
    parser.add_argument('--emin', type=float, default=None,
                        help='Set energy minium on y axis.')
    parser.add_argument('--gap', type=float, default=0,
                        help='Set gap between bars.')
    parser.add_argument('--bar-width', type=float, dest='bar_width', default=3,
                        help='Set the width per bar for each compound.')
    parser.add_argument('--font', default=None, help='Font to use.')
    parser.add_argument('--font-size', type=float, dest='label_size',
                        default=15, help='Set font size all labels.')
    parser.add_argument('--name-colour', dest='name_colour', default='w',
                        help='Set the colour for the compound name.')
    parser.add_argument('--fade-cb', action='store_true', dest='fade_cb',
                        help='Apply a fade to the conduction band segments.')
    parser.add_argument('--dpi', default=400,
                        help='Dots-per-inch for file output.')
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
        sys.exit()

    output_file = args.output

    if args.filename:
        data, settings = read_config(args.filename)
    else:
        data = [{'name': name, 'ip': ip, 'ea': ea} for name, ip, ea in
                zip(args.name.split(','), map(float, args.ip.split(',')),
                    map(float, args.ea.split(',')))]
        settings = {}

    properties = vars(args)
    remove_keys = ('filename', 'ip', 'ea', 'name', 'output', 'dpi')
    for key in remove_keys:
        properties.pop(key, None)
    properties.update(settings)

    plt = get_plot(data, **properties)
    plt.savefig(output_file, dpi=400, bbox_inches='tight')


if __name__ == "__main__":
    main()
