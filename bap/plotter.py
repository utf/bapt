# coding: utf-8
# Copyright (c) Alex Ganose
# Distributed under the terms of the MIT License.

from bap import pretty_plot, gbar

from matplotlib.ticker import MaxNLocator

cb_cmap = [
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
                 bar_width=3, show_axis=False, plt=None, fonts=None):

        width = bar_width/2. * len(self.data) if not width else width
        emin = self.emin if not emin else emin

        plt = pretty_plot(width=width, height=height, plt=plt, fonts=fonts)
        ax = plt.gca()

        for i, compound in enumerate(self.data):
            gbar(ax, i * bar_width, -compound['ip'], bottom=emin,
                 bar_width=bar_width, show_edge=True, gradient=None)
            gbar(ax, i * bar_width, -compound['ea'], bar_width=bar_width,
                 show_edge=True, gradient=None)

        ax.set_ylim((self.emin, 0))
        ax.set_xlim((0, len(self.data) * bar_width))
        ax.set_xticks([])

        if show_axis:
            ax.yaxis.set_major_locator(MaxNLocator(5))
        else:
            ax.axis('off')
        return plt
