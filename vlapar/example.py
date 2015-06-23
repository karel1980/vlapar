import vlapar
import os

def eg1():
    if not os.path.exists('cache'):
        print "cache dir does not exist. Did you run 'vlapar getmeta' first?"
    schv = vlapar.meta.load_meta('SCHV')
    print schv.groupby(['legislatuur','minister','status']).count()
