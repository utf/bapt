"""
Vaspy: SMTG utils for working with Vasp
"""

from os.path import abspath, dirname
from setuptools import setup, find_packages

project_dir = abspath(dirname(__file__))

setup(
    name='bap',
    version='1.0.0',
    description='Band alignment plotting tools',
    long_description="""
Get yourself some nice band alignment diagrams
""",
    url="https://github.com/utf/bap",
    author="Alex Ganose",
    author_email="Alex Ganose",
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics'
        ],
    keywords='chemistry dft band alignment ionisation potential electron',
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib'],
    #entry_points={'console_scripts': [
    #                  'vaspy-bandgen = ba.cli.bandgen:main',
    #                  'vaspy-bandplot = vaspy.cli.bandplot:main',
    #                  'vaspy-bandstats = vaspy.cli.bandstats:main',
    #                  'vaspy-dosplot = vaspy.cli.dosplot:main',
    #                  'vaspy-kgen = vaspy.cli.kgen:main',
    #                  'vaspy-optics = vaspy.cli.optics:main']}
    )
