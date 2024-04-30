# coding: utf-8
# Copyright (c) Alex Ganose
# Distributed under the terms of the MIT License.

from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap


cb_colours = [(247/255., 148/255., 51/255.), (251/255., 216/255., 181/255.)]
vb_colours = [(23/255., 71/255., 158/255.), (174/255., 198/255., 242/255.)]
cb_cmap = LinearSegmentedColormap.from_list('cb', cb_colours, N=200)
vb_cmap = LinearSegmentedColormap.from_list('vb', vb_colours, N=200)

default_fonts = ['Whitney Pro', 'Helvetica', 'Arial', 'Whitney Book'
                 'Liberation Sans', 'Andale Sans']
_ticklabelsize = 15
_labelsize = 18
_ticksize = 5
_linewidth = 1.


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
                   labelsize=_ticklabelsize, pad=4, direction='in',
                   top='off', bottom='off', right='on', left='on')
    ax.tick_params(which='minor', size=_ticksize/2, width=_linewidth,
                   direction='in', top='off', bottom='off')

    ax.set_title(ax.get_title(), size=20)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(_linewidth)

    ax.set_xlabel(ax.get_xlabel(), size=_labelsize)
    ax.set_ylabel(ax.get_ylabel(), size=_labelsize)

    fonts = default_fonts if fonts is None or fonts == [None] else fonts + default_fonts

    rc('font', **{'family': 'sans-serif', 'sans-serif': fonts})
    rc('text', usetex=False)
    rc('pdf', fonttype=42)
    rc('mathtext', fontset='stixsans')
    rc('legend', handlelength=2)
    return plt


def cbar(ax, left, top, face_colour, bar_width=3, bottom=0,
         show_edge=True, edge_colour='k', edge_zorder=5):
    X = [[.6, .6], [.7, .7]]
    right = left + bar_width
    patch = Rectangle((left, top), bar_width, bottom-top, fill=True,
                           clip_on=False, facecolor=face_colour,
                          )
    ax.add_patch(patch)

    if show_edge:
        border = Rectangle((left, top), bar_width, bottom-top, fill=False,
                           lw=_linewidth, edgecolor=edge_colour, clip_on=False,
                           zorder=edge_zorder)
        ax.add_patch(border)

def gbar(ax, left, top, bar_width=3, bottom=0, gradient=vb_cmap,
         show_edge=True, edge_colour='k', edge_zorder=5):
    X = [[.6, .6], [.7, .7]]
    right = left + bar_width
    ax.imshow(X, interpolation='bicubic', cmap=gradient,
              extent=(left, right, bottom, top), alpha=1)

    if show_edge:
        border = Rectangle((left, top), bar_width, bottom-top, fill=False,
                           lw=_linewidth, edgecolor=edge_colour, clip_on=False,
                           zorder=edge_zorder)
        ax.add_patch(border)


def fadebar(ax, left, top, bar_width=3, bottom=0, zorder=3):
    fade = Rectangle((left, top), bar_width, bottom-top, alpha=0.5, color='w',
                     clip_on=False, zorder=zorder)
    ax.add_patch(fade)


def dashed_arrow(ax, x, y, dx, dy, colour='k', line_width=_linewidth,
                 start_head=True, end_head=True):
    length = 0.25
    width = 0.2
    ax.plot([x, x + dx], [y, y + dy], c=colour, ls='--', lw=line_width,
            dashes=(8, 4.3))
    if start_head:
        ax.arrow(x, y + length, 0, -length, head_width=width,
                 head_length=length, fc=colour, ec=colour, overhang=0.15,
                 length_includes_head=True, lw=line_width)
    if end_head:
        ax.arrow(x + dx, y + dy - length, 0, length, head_width=width,
                 head_length=length, fc=colour, ec=colour, overhang=0.15,
                 length_includes_head=True, lw=line_width)
