import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description. 
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "vlapar",
    version = "0.0.1",
    author = "Karel Vervaeke",
    author_email = "karel@vervaeke.info",
    description = ("An analysis of the flemish parliament's open data"),
    entry_points={
        'console_scripts': [ 'vlapar = vlapar.cli:main' ]
    },
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=['pandas'],
    license = "MIT",
    keywords = "open data flanders belgium",
    url = "http://packages.python.org/vlapar",
    packages=['vlapar', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License"
    ],
)
