# coding: utf-8
# Copyright (c) Alex Ganose
# Distributed under the terms of the MIT License.

from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap


cb_colours = [(247/255., 148/255., 51/255.), (251/255., 216/255., 181/255.)]
vb_colours = [(23/255., 71/255., 158/255.), (174/255., 198/255., 242/255.)]
cb_cmap = LinearSegmentedColormap.from_list('cb', cb_colours, N=200)
vb_cmap = LinearSegmentedColormap.from_list('vb', vb_colours, N=200)

default_fonts = ['Whitney Book Extended', 'Arial', 'Whitney Book', 'Helvetica',
                 'Liberation Sans', 'Andale Sans']
_ticklabelsize = 18
_labelsize = 18
_ticksize = 6
_linewidth = 1.3


def pretty_plot(width=5, height=5, plt=None, dpi=400, fonts=None):
    """Initialise a matplotlib plot with sensible defaults for publication.


    Args:
        width (float): Width of plot in inches. Defaults to 8 in.
        height (float): Height of plot in inches. Defaults to 8 in.
        plt (matplotlib.pyplot): If plt is supplied, changes will be made to an
            existing plot. Otherwise, a new plot will be created.
        dpi (int): Sets dot per inch for figure. Defaults to 400.
        fonts (list): A list of preferred fonts. If these are not found the
            default fonts will be used.

    Returns:
        Matplotlib plot object with properly sized fonts.
    """

    from matplotlib import rc

    if plt is None:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(width, height), facecolor="w", dpi=dpi)
        ax = plt.gca()

    ax = plt.gca()

    ax.tick_params(width=_linewidth, size=_ticksize)
    ax.tick_params(which='major', size=_ticksize, width=_linewidth,
                   labelsize=_ticklabelsize, pad=10, direction='in',
                   top='off', bottom='off')
    ax.tick_params(which='minor', size=_ticksize/2, width=_linewidth,
                   direction='in', top='off', bottom='off')

    ax.set_title(ax.get_title(), size=20)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(_linewidth)

    ax.set_xlabel(ax.get_xlabel(), size=_labelsize)
    ax.set_ylabel(ax.get_ylabel(), size=_labelsize)

    fonts = default_fonts if fonts is None else fonts + default_fonts

    rc('font', **{'family': 'sans-serif', 'sans-serif': fonts})
    rc('text', usetex=False)
    rc('pdf', fonttype=42)
    rc('mathtext', fontset='stixsans')
    rc('legend', handlelength=2)
    return plt


def gbar(ax, left, top, bar_width=2, bottom=0, gradient=vb_cmap, show_edge=True,
         fade=False):
    X = [[.6, .6], [.7, .7]]
    right = left + bar_width
    ax.imshow(X, interpolation='bicubic', cmap=gradient,
              extent=(left, right, bottom, top), alpha=1)

    if show_edge:
        border = Rectangle((left, top), bar_width, bottom-top, fill=False,
                           lw=_linewidth, edgecolor='k')
        ax.add_patch(border)


def dashed_arrow(ax, x, y, dx, dy, colour='k', line_width=_linewidth):
    length = 0.25
    width = 0.2
    ax.plot([x, x + dx], [y, y + dy], c=colour, ls='--', lw=line_width,
            dashes=(8, 4.3))
    ax.arrow(x + dx, y + dy - length, 0, length, head_width=width,
             head_length=length, fc=colour, ec=colour, overhang=0.15,
             length_includes_head=True, lw=line_width)


def read_config(filename):
    try:
        import ruamel.yaml as yaml
    except ImportError:
        import yaml

    with open(filename, 'r') as f:
        config = yaml.load(f)
    band_edge_data = config['compounds']
    return band_edge_data
