import vlapar
import os

def eg1():
    if not os.path.exists('cache'):
        print "cache dir does not exist. Did you run 'vlapar getmeta' first?"
    schv = vlapar.meta.MetaFetcher("cache").load_meta('soort','SCHV')
    print schv.groupby(['legislatuur','minister','status'])['status'].count()
