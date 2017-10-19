# coding: utf-8
# Copyright (c) Alex Ganose
# Distributed under the terms of the MIT License.

from bap import pretty_plot, gbar, vb_cmap, cb_cmap, dashed_arrow

from matplotlib.ticker import MaxNLocator


class BandAlignmentPlotter(object):

    def __init__(self, band_edge_data):
        """General purpose band alignment plotter object.

        Args:
            band_edge_data (list): A list of dictionary items containing the
                keys: 'name', 'ip', 'ea'. Name should be a string, and ip and
                ea are floats

        Returns:
            Band alignment plotter object.
        """
        self.data = band_edge_data
        self.emin = -max([d['ip'] for d in self.data]) - 2

    def get_plot(self, height=5, width=None, emin=None, colours=None,
                 bar_width=3, show_axis=False, label_size=15, plt=None,
                 fonts=None):

        width = bar_width/2. * len(self.data) if not width else width
        emin = self.emin if not emin else emin

        plt = pretty_plot(width=width, height=height, plt=plt, fonts=fonts)
        ax = plt.gca()

        pad = 2. / emin
        for i, compound in enumerate(self.data):
            x = i * bar_width
            ip = -compound['ip']
            ea = -compound['ea']

            gbar(ax, x, ip, bottom=emin, bar_width=bar_width, show_edge=True,
                 gradient=vb_cmap)
            gbar(ax, x, ea, bar_width=bar_width, show_edge=True,
                 gradient=cb_cmap)
            dashed_arrow(ax, x + bar_width/6., ip, 0, -ip + pad/5, colour='k',
                         line_width=1.3)

            ax.text(x + bar_width/2., ip + pad, compound['name'], ha='center',
                    va='top', size=label_size, color='w')
            ax.text(x + bar_width/4., pad * 2, '{:.1f} eV'.format(compound['ip']),
                    ha='left', va='top', size=label_size+1, color='k')

        ax.set_ylim((emin, 0))
        ax.set_xlim((0, len(self.data) * bar_width))
        ax.set_xticks([])

        if show_axis:
            ax.yaxis.set_major_locator(MaxNLocator(5))
        else:
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.yaxis.set_visible(False)

        ax.set_title('Vacuum Level', size=18)
        ax.set_xlabel('Valence Band', size=18)
        #ax.text(0.5, 0, 'Valence Band', ha='center', transform=ax.transAxes,
        #        va='top', size=18)
        return plt
