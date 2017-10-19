README
======

Introduction
------------

Bap is a tool for generating publication-ready band alignment plots.


Usage
-----

Bap can be used via the command-line or python api. For the full
documentation of the command-line flags, please use the built-in help:

    bap -h

The bap command-line can be controlled through command-line flags or
a settings file. The settings file provides considerably more flexibility
for things like custom gradients and fading effects.

A basic usage of the command-line interface:

    bap --name "ZnO,MOF-5,HKUST-1,ZIF-8" --ip 7.7,7.3,6.0,6.4 --ea 4.4,2.7,5.1,1.9

produces a plot that is ready to go into any publication:

<img src="https://raw.githubusercontent.com/utf/bap/master/examples/command-line.png" height="350">

A more advanced plot, generated using the `examples/gradients.yaml` config
file, allows for additional effects:

    bap --filename examples/gradients.yaml

<img src="https://raw.githubusercontent.com/utf/bap/master/examples/gradients.png" height="350">


Requirements
------------

Bap is currently compatible with Python 2.7 and Python 3.4. Matplotlib is required 
for plotting and PyYAML is needed for config files.

Bap uses Pip and setuptools for installation. You *probably* already
have this; if not, your GNU/Linux package manager will be able to oblige
with a package named something like ``python-setuptools``. On Max OSX
the Python distributed with [Homebrew](<http://brew.sh>) includes
setuptools and Pip.


Installation
------------

First clone the this repository, then, from the directory containing this README::

    pip3 install --user .


License
-------

Bap is made available under the MIT License.
