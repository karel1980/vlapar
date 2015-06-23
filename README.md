
# What

Tools for analysing the Flemish parliament's open data.

# Installation

    python setup.py install

If you plan to develop the tool, run this instead:

    python setup.py develop --user

# Obtaining metadata

To obtain a local copy of the metadata, run

    vlapar getmeta

this will create a directory 'cache' and download metadata in json format into that directory.

# Analysing the data

Use the source luke. Here's an example of what you can do with it: (requires pandas)

    vlapar example

