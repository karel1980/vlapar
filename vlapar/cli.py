
import sys
import argparse

import vlapar.meta

def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    getmeta = subparsers.add_parser('getmeta')
    getmeta.set_defaults(func=vlapar.meta.download_all)

    #getdata = subparsers.add_parser('getdata')

    example = subparsers.add_parser('example')
    example.set_defaults(func=vlapar.example.eg1)

    args = parser.parse_args(sys.argv[1:])

    args.func()
