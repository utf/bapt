# coding: utf-8
# Copyright (c) Alex Ganose
# Distributed under the terms of the MIT License.

from bapt.plotting import (pretty_plot, gbar, vb_cmap, cb_cmap, dashed_arrow,
                           _linewidth, fadebar)

from matplotlib.ticker import MaxNLocator
from matplotlib.colors import LinearSegmentedColormap


def get_plot(data, height=5, width=None, emin=None, colours=None,
             bar_width=3, show_axis=False, label_size=15, plt=None,
             fonts=None, show_ea=False, name_colour='w', fade_cb=False):

    width = bar_width/2. * len(data) if not width else width
    emin = emin if emin else -max([d['ip'] for d in data]) - 2

    plt = pretty_plot(width=width, height=height, plt=plt, fonts=fonts)
    ax = plt.gca()

    pad = 2. / emin
    for i, compound in enumerate(data):
        x = i * bar_width
        ip = -compound['ip']
        ea = -compound['ea']

        fade = 'fade' in compound and compound['fade']
        edge_c_cb = '#808080' if fade or fade_cb else 'k'
        edge_c_vb = '#808080' if fade else 'k'
        edge_z = 4 if fade else 5

        vc = vb_cmap if 'vb_gradient' not in compound else \
            compound['vb_gradient']
        cc = cb_cmap if 'cb_gradient' not in compound else \
            compound['cb_gradient']

        gbar(ax, x, ip, bottom=emin, bar_width=bar_width, show_edge=True,
             gradient=vc, edge_colour=edge_c_vb, edge_zorder=edge_z)
        gbar(ax, x, ea, bar_width=bar_width, show_edge=True,
             gradient=cc, edge_colour=edge_c_cb, edge_zorder=edge_z)

        if show_ea:
            dashed_arrow(ax, x + bar_width/6., ea - pad/3, 0,
                         -ea + 2 * pad/3, colour='k', line_width=_linewidth)
            dashed_arrow(ax, x + bar_width/6., ip - pad/3, 0,
                         ea-ip + 2 * pad/3, colour='k', end_head=False,
                         line_width=_linewidth)
            ax.text(x + bar_width/4., ip - pad/2,
                    '{:.1f} eV'.format(compound['ip']), ha='left',
                    va='bottom', size=label_size, color='k', zorder=2)
            ax.text(x + bar_width/4., pad * 2,
                    '{:.1f} eV'.format(compound['ea']), ha='left', va='top',
                    size=label_size, color='k', zorder=2)
        else:
            dashed_arrow(ax, x + bar_width/6., ip - pad/3, 0,
                         -ip + 2 * pad/3, colour='k', line_width=_linewidth)
            ax.text(x + bar_width/4., pad * 2,
                    '{:.1f} eV'.format(compound['ip']), ha='left', va='top',
                    size=label_size, color='k', zorder=2)

        ax.text(x + bar_width/2., ip + pad, compound['name'], zorder=2,
                ha='center', va='top', size=label_size, color=name_colour)

        if fade:
            fadebar(ax, x, emin, bottom=0)
        elif fade_cb:
            fadebar(ax, x, ea, bottom=0, zorder=1)

    ax.set_ylim((emin, 0))
    ax.set_xlim((0, len(data) * bar_width))
    ax.set_xticks([])

    if show_axis:
        ax.yaxis.set_major_locator(MaxNLocator(5))
    else:
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.yaxis.set_visible(False)

    ax.set_title('Vacuum Level', size=18)
    ax.set_xlabel('Valence Band', size=18)
    return plt


def read_config(filename):
    try:
        import ruamel.yaml as yaml
    except ImportError:
        import yaml

    with open(filename, 'r') as f:
        config = yaml.load(f)

    settings = config['settings'] if 'settings' in config else {}
    gradient_data = config['gradients'] if 'gradients' in config else []
    gradients = {}
    for d in gradient_data:
        g = LinearSegmentedColormap.from_list(d['id'], [d['start'], d['end']],
                                              N=200)
        gradients[d['id']] = g

    band_edge_data = config['compounds']
    for compound in band_edge_data:
        if 'gradient' in compound:
            ids = map(int, compound['gradient'].split(','))
            compound.pop('gradient', None)
            if len(ids) == 1:
                compound['vb_gradient'] = gradients[ids[0]]
                compound['cb_gradient'] = gradients[ids[0]]
            else:
                compound['vb_gradient'] = gradients[ids[0]]
                compound['cb_gradient'] = gradients[ids[1]]
    return band_edge_data, settings
