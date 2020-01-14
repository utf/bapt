# coding: utf-8
# Copyright (c) Alex Ganose
# Distributed under the terms of the MIT License.

import sys
import argparse

from . import read_config, get_plot, get_plot_novac

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
                        help='List of compound names (comma seperated). ' +
                        'Must be used in conguction with --ip and --ea. ' +
                        'Use $_x$ and $^y$ for subscript and superscript.')
    parser.add_argument('-i', '--ip',
                        help='List of ionisation potentials (comma separated).')
    parser.add_argument('-e', '--ea',
                        help='List of electron affinities (comma separated).')
    parser.add_argument('-c', '--cbo', default=None,
                        help='List of conduction band offsets (comma separated). ' +
                        '(Relative to first compound)(-> No vacuum alignment)')
    parser.add_argument('-v', '--vbo', default=None,
                        help='List of valence band offsets (comma separated). ' +
                        '(Relative to first compound)(-> No vacuum alignment)')
    parser.add_argument('-b', '--band-gap', dest='band_gap',
                        help='List of band gaps (comma separated).')
    parser.add_argument('-o', '--output', default='alignment.pdf',
                        help='Output file name (defaults to alignment.pdf).')
    parser.add_argument('--show-ea', action='store_true', dest='show_ea',
                        help='Display the electron affinity value.')
    parser.add_argument('--hide-cbo', action='store_true', dest='hide_cbo',
                        help='Hide the conduction band offsets.')
    parser.add_argument('--hide-vbo', action='store_true', dest='hide_vbo',
                        help='Hide the valence band offsets.')
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
    if not args.filename and not (args.name or args.ip or args.ea or args.band_gap or args.cbo or args.vbo):
        emsg = "ERROR: no arguments specified."
    elif not args.filename and not (args.ip or args.ea) and \
            not (args.name and args.band_gap and (args.cbo or args.vbo)):
        emsg = "ERROR: --name, --band-gap and --cbo or --vbo flags must specified concurrently."
    elif not args.filename and not (args.cbo or args.vbo or args.band_gap) and \
            not (args.name and args.ip and args.ea):
        emsg = "ERROR: --name, --ip and --ea flags must specified concurrently."
    elif not args.filename and (args.cbo and args.vbo):
        emsg = "ERROR: cbo and vbo specified simultaneously."
    elif args.filename and (args.name or args.ip or args.ea or args.band_gap or args.cbo or args.vbo):
        emsg = "ERROR: filename and name/ip/ea/cbo/vbo specified simultaneously."

    if emsg:
        print(emsg)
        sys.exit()

    output_file = args.output

    if args.filename:
        data, settings = read_config(args.filename)
        for item in data:
            if 'cbo' in item:
                item['vbo'] = data[0]['band_gap'] - item['band_gap'] + item['cbo']
            if 'vbo' in item:
                item['cbo'] = -data[0]['band_gap'] + item['band_gap'] + item['vbo']

    else:
        for k, v in {'cbo': args.cbo, 'vbo': args.vbo}.items():
            if v:
                data = [{'name': name, 'band_gap': band_gap, k: c_or_v_bo} for name, band_gap, c_or_v_bo in
                        zip(args.name.split(','), map(float, args.band_gap.split(',')),
                            [0] + list(map(float, v.split(','))))]
                for item in data:
                    if k is 'cbo':
                        item['vbo'] = data[0]['band_gap'] - item['band_gap'] + item['cbo']
                    if k is 'vbo':
                        item['cbo'] = -data[0]['band_gap'] + item['band_gap'] + item['vbo']
        if args.ip:
            data = [{'name': name, 'ip': ip, 'ea': ea} for name, ip, ea in
                    zip(args.name.split(','), map(float, args.ip.split(',')),
                        map(float, args.ea.split(',')))]

        settings = {}

    properties = vars(args)
    remove_keys = ('filename', 'ip', 'ea', 'band_gap', 'cbo',
                   'vbo', 'name', 'output', 'dpi')
    for key in remove_keys:
        properties.pop(key, None)
    properties.update(settings)

    if 'vbo' in data[0]:  # no vacuum alignment
        plt = get_plot_novac(data, **properties)
    else:
        [properties.pop(key, None) for key in ['hide_cbo', 'hide_vbo']]
        plt = get_plot(data, **properties)
    plt.savefig(output_file, dpi=400, bbox_inches='tight')


if __name__ == "__main__":
    main()
