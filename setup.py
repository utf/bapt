"""
Vaspy: SMTG utils for working with Vasp
"""

from os.path import abspath, dirname
from setuptools import setup, find_packages

project_dir = abspath(dirname(__file__))

setup(
    name='bapt',
    version='1.0.0',
    description='Band alignment plotting tool',
    long_description="""
Get yourself some nice band alignment diagrams
""",
    url="https://github.com/utf/bapt",
    author="Alex Ganose",
    author_email="alexganose@googlemail.com",
    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics'
        ],
    keywords='chemistry dft band alignment ionisation potential electron',
    packages=find_packages(),
    install_requires=['matplotlib'],
    entry_points={'console_scripts': ['bapt = bapt.cli:main']}
)
