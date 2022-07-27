# coding: utf-8
# Copyright (c) Alex Ganose
# Distributed under the terms of the MIT License.

from .plotting import (pretty_plot, gbar, cbar, vb_cmap, cb_cmap, dashed_arrow, _linewidth, fadebar)

from matplotlib.ticker import MaxNLocator, MultipleLocator
from matplotlib.colors import LinearSegmentedColormap


def get_plot(data, height=5, width=None, emin=None, colours=None,
             bar_width=3, show_axis=False, label_size=15, plt=None, gap=0.5,
             font=None, show_ea=False, name_colour='w', fade_cb=False, gradients=True, photocat_hlines=False):

    width = (bar_width/2. + gap/2.) * len(data) if not width else width
    emin = emin if emin else -max([d['ip'] for d in data]) - 2

    plt = pretty_plot(width=width, height=height, plt=plt, fonts=[font])
    ax = plt.gca()

    pad = 2. / emin
    for i, compound in enumerate(data):
        x = i * (bar_width + gap)
        ip = -compound['ip']
        ea = -compound['ea']

        fade = 'fade' in compound and compound['fade']
        edge_c_cb = '#808080' if fade or fade_cb else 'k'
        edge_c_vb = '#808080' if fade else 'k'
        edge_z = 4 if fade else 5

        if gradients:
            vg = vb_cmap if 'vb_gradient' not in compound else \
                compound['vb_gradient']
            cg = cb_cmap if 'cb_gradient' not in compound else \
                compound['cb_gradient']

            gbar(ax, x, ip, bottom=emin, bar_width=bar_width, show_edge=True,
                gradient=vg, edge_colour=edge_c_vb, edge_zorder=edge_z)
            gbar(ax, x, ea, bar_width=bar_width, show_edge=True,
                gradient=cg, edge_colour=edge_c_cb, edge_zorder=edge_z)

        else: 
            vc = '#219ebc' if 'vb_colour' not in compound else \
                compound['vb_colour']
            cc ='#fb8500' if 'cb_colour' not in compound else \
                compound['cb_colour']

            cbar(ax, x, ip, vc, bottom=emin, bar_width=bar_width, show_edge=True, 
                edge_colour=edge_c_vb, edge_zorder=edge_z)
            cbar(ax, x, ea, cc, bar_width=bar_width, show_edge=True, 
                edge_colour=edge_c_vb, edge_zorder=edge_z)
            
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
            fadebar(ax, x, emin, bar_width=bar_width, bottom=0)
        elif fade_cb:
            fadebar(ax, x, ea, bar_width=bar_width, bottom=0, zorder=1)
    
    ax.set_ylim((emin, 0))
    ax.set_xlim((0, (len(data) * bar_width) + ((len(data) - 1) * gap)))

    if photocat_hlines: 
        end = (len(data) * bar_width) + ((len(data) - 1) * gap)
        ax.hlines([-4.44, -5.67], 0, end, colors=['#808080', '#808080'], zorder=0, linewidths=1, linestyles='dotted', label=['H3O$^+$/H2', 'H$_2$O/O$_2$'])
        plt.text(end+0.1, -4.44, '[H$^+$/H$_2$]', va='center', size=label_size)
        plt.text(end+0.1, -5.67, '[H$_2$O/O$_2$]', va='center', size=label_size)

    ax.set_xticks([])

    if show_axis:
        ax.set_ylabel("Energy (eV)", size=label_size)
        ax.yaxis.set_major_locator(MaxNLocator(5))
        for spine in ax.spines.values():
            spine.set_zorder(5)
    else:
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.yaxis.set_visible(False)

    ax.set_title('Vacuum Level', size=label_size)
    ax.set_xlabel('Valence Band', size=label_size)
    return plt


def read_config(filename):
    import yaml

    with open(filename, 'r') as f:
        # stop showing yaml warning
        config = yaml.load(f, Loader=yaml.FullLoader)

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
            ids = list(map(int, compound['gradient'].split(',')))
            compound.pop('gradient', None)
            if len(ids) == 1:
                compound['vb_gradient'] = gradients[ids[0]]
                compound['cb_gradient'] = gradients[ids[0]]
            else:
                compound['vb_gradient'] = gradients[ids[0]]
                compound['cb_gradient'] = gradients[ids[1]]
    return band_edge_data, settings


def get_plot_novac(data, height=5, width=None, emin=None, emax=None,
                   colours=None, bar_width=3, show_axis=False, hide_cbo=False,
                   hide_vbo=False, label_size=15, plt=None, gap=0.5, font=None,
                   show_ea=False, name_colour='w', fade_cb=False, gradients=True):

    width = (bar_width/2. + gap/2.) * len(data) if not width else width
    emin = emin if emin else min([d['vbo'] for d in data]) - 2
    emax = emax if emax else max([d['vbo'] + d['band_gap'] for d in data]) + 2

    plt = pretty_plot(width=width, height=height, plt=plt, fonts=[font])
    ax = plt.gca()

    pad = - (emax - emin) / 20
    for i, compound in enumerate(data):
        x = i * (bar_width + gap)
        ip = compound['vbo']
        ea = compound['vbo'] + compound['band_gap']

        fade = 'fade' in compound and compound['fade']
        edge_c_cb = '#808080' if fade or fade_cb else 'k'
        edge_c_vb = '#808080' if fade else 'k'
        edge_z = 4 if fade else 5
        
        if gradients: 
            vc = vb_cmap if 'vb_gradient' not in compound else \
                compound['vb_gradient']
            cc = cb_cmap if 'cb_gradient' not in compound else \
                compound['cb_gradient']

            gbar(ax, x, ip, bottom=emin, bar_width=bar_width, show_edge=True,
                gradient=vc, edge_colour=edge_c_vb, edge_zorder=edge_z)
            gbar(ax, x, ea, bottom=emax, bar_width=bar_width, show_edge=True,
                gradient=cc, edge_colour=edge_c_cb, edge_zorder=edge_z)
        else: 
            vc = '#219ebc' if 'vb_colour' not in compound else \
                compound['vb_colour']
            cc ='#fb8500' if 'cb_colour' not in compound else \
                compound['cb_colour']

            cbar(ax, x, ip, vc, bottom=emin, bar_width=bar_width, show_edge=True,       
                edge_colour=edge_c_vb, edge_zorder=edge_z)
            cbar(ax, x, ea, cc, bottom=emax, bar_width=bar_width, show_edge=True, 
                edge_colour=edge_c_vb, edge_zorder=edge_z)

        dashed_arrow(ax, x + bar_width/6., ip - pad/3, 0,
                     ea-ip + 2 * pad/3, colour='k', line_width=_linewidth)
        ax.text(x + bar_width/4., ip + compound['band_gap']/2,
                '{:.2f} eV'.format(compound['band_gap']), ha='left',
                va='center', size=label_size, color='k', zorder=2)

        t = ax.text(x + bar_width/2., ip + pad / 2, compound['name'], zorder=2,
                    ha='center', va='top', size=label_size, color=name_colour)

        # use renderer to get position of compound label text
        renderer = plt.gcf().canvas.get_renderer()
        bb = t.get_window_extent(renderer=renderer)
        inv = ax.transData.inverted()
        y1 = inv.transform([bb.y0, bb.y1 + 2 * bb.height])[1]
        if i > 0:
            if not hide_vbo:
                vbo = compound['vbo'] - data[i-1]['vbo']
                ax.text(x + bar_width/2., y1,
                        "{:+.2f} eV".format(vbo), zorder=2, ha='center',
                        va='top', size=label_size, color=name_colour)

            if not hide_cbo:
                cbo = compound['cbo'] - data[i-1]['cbo']
                ax.text(x + bar_width/2., ea - pad / 4,
                        "{:+.2f} eV".format(cbo), zorder=2, ha='center',
                        va='bottom', size=label_size, color=name_colour)

        if fade:
            fadebar(ax, x, emin, bar_width=bar_width, bottom=emax)
        elif fade_cb:
            fadebar(ax, x, ea, bar_width=bar_width, bottom=emax, zorder=1)

    ax.set_ylim((emin, emax))
    ax.set_xlim((0, (len(data) * bar_width) + ((len(data) - 1) * gap)))
    ax.set_xticks([])

    if show_axis:
        ax.set_ylabel("Energy (eV)", size=label_size)
        ax.yaxis.set_major_locator(MultipleLocator(1))
        for spine in ax.spines.values():
            spine.set_zorder(5)
        ax.tick_params(which='major', width=_linewidth)
        ax.tick_params(which='minor', right='on')
        ax.yaxis.set_minor_locator(MultipleLocator(0.5))
    else:
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.yaxis.set_visible(False)

    ax.set_title('Conduction Band', size=label_size)
    ax.set_xlabel('Valence Band', size=label_size)
    return plt
