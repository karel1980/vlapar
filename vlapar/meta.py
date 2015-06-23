import os
import codecs
import requests
import json
import pandas as pd
import glob

#FIXME: this list is incomplete
types = [ 'PI', 'VI', 'JLN', 'SCHV' ]

def download_meta(doctype, start_page=1):
    """ Download metadata for a given document type (PI, VI, JLN, SCHV)
    BUGS: the service seems to be limited to 1000 results (10 pages of 100). Create a drill down mechanism
    which starts over with additional filters to break up queries into manageable parts.  To do this we can include
    additional filters based on observed metatag values
    """

    if not os.path.exists('cache'):
        os.makedirs('cache')

    for page in range(start_page,50):
        print "Fetching %s page %d"%(doctype,page,)
        resp = requests.get('http://ws.vlpar.be/e/gsa/resource/search/query/inmeta%%3Asoort%%3D%s?page=%d&max=100'%(doctype,page,))
        #print resp.text
        # Stop when we get empty results
        if 'result' not in resp.json() or len(resp.json()['result']) == 0:
            return

        with codecs.open("cache/%s-%03d.json"%(doctype,page),'w','utf-8') as f:
            f.write(resp.text)

def download_all():
    """ Download all metadata. Subject to the limitation documented in get_meta_for_type.  """

    for doctype in types:
        download_meta(doctype)

def load_meta(doctype):
    """ Loads metadata for given type as dataframe (type = PI, VI, ...) """

    # TODO: allow customising tags & fields to include in dataframe? (predefined sets? load everything?)
    tags = ['legislatuur','minister','vraagsteller','status']
    return _get_dataframe(glob.glob('cache/%s-*.json'%(doctype)), tags)

def _get_dataframe(paths, metatags):
    """ Reads a path or buffer and converts it into a dataframe ready for analysis """
    all_rows = []
    for path in paths:
        obj = json.load(open(path))
        rows = obj['result']
        all_rows += [ _record_to_row(record, metatags) for record in rows ]
        
    return pd.DataFrame(all_rows, columns=metatags)

def _record_to_row(record, metatags):
    """ Converts a record into a row for our dataframe """

    # Get metatags as dict
    # If key occurs more than once earlier ones are dropped
    tags = dict([(meta['name'],meta['value']) for meta in record['metatags']['metatag']])

    return tuple([tags.get(tag, None) for tag in metatags])


