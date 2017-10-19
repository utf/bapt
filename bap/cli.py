# coding: utf-8
# Copyright (c) Alex Ganose
# Distributed under the terms of the MIT License.

from bap.plotter import BandAlignmentPlotter

data = [{'name': 'ZnO', 'ea': 4.4, 'ip': 7.7},
        {'name': 'MOF-5', 'ea': 2.7, 'ip': 7.3},
        {'name': 'HKUST-1', 'ea': 5.1, 'ip': 6.0},
        {'name': 'ZIF-8', 'ea': 1.3, 'ip': 4.7},
        {'name': 'COF-1M', 'ea': 2.9, 'ip': 5.9}]

baper = BandAlignmentPlotter(data)
plt = baper.get_plot()
plt.savefig('plt.pdf')
