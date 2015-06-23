import os
import codecs
import requests
import json
import pandas as pd
import glob

MAX_PAGE_COUNT=10
MAX_PAGE_SIZE=100

#FIXME: this list is incomplete
types = [ 'PI', 'VI', 'JLN', 'SCHV', 'DBT' ]

def download_all():
    """ Fetches different document types (maximum 1000 per type """

    MetaFetcher('cache').fetch('soort',types)

class MetaFetcher:
    def __init__(self, cachedir):
        self.cachedir = cachedir
        if not os.path.exists(self.cachedir):
            os.makedirs(self.cachedir)
        pass

    def fetch(self, metatag, values):
        """ Tries to retrieve all documents matching start_criteria."""

        limit = MAX_PAGE_SIZE * MAX_PAGE_COUNT

        for value in values:
            # TODO: instead of fetching one pgae beforehand
            # we could simply check if the last page haad MAX_PAGE_SIZE results.
            # (more accurate, but we can only warn at the end instead of at the beginning
            response = self.fetch_page(metatag, value, 0)

            count = 0 if response['count'] == '' else int(response['count'])
            if count > limit:
                print "Warning: %s:%s yields > 1000 results (%s)"%(metatag,value,response['count'])

            if count == 0: continue

            for page in range(1,10):
                response = self.fetch_page(metatag, value, page)
                count = 0 if response['count'] == '' else int(response['count'])
                if len(response['result']) < MAX_PAGE_SIZE:
                    # We've hit the last page
                    break

    def fetch_page(self, metatag, value, page):
        url_format = "http://ws.vlpar.be/e/gsa/resource/search/query/inmeta%%3A%s%%3D%s?page=%d&max=%d"
        url = url_format%(metatag,value,page,MAX_PAGE_SIZE)
        resp = requests.get(url)
        with codecs.open(os.path.join(self.cachedir,"%s:%s-%02d.json"%(metatag,value,page)),'w','utf-8') as f:
            f.write(resp.text)
        return resp.json()

    def load_meta(self, metatag, value):
        """ Loads metadata for given type as dataframe (type = PI, VI, ...) """

        # TODO: allow customising tags & fields to include in dataframe? (predefined sets? load everything?)
        tags = ['legislatuur','minister','vraagsteller','status','soort','datum','thema','company','source','word count']
        files = glob.glob(os.path.join(self.cachedir, "%s:%s-*.json"%(metatag,value)))
        return self._get_metatag_dataframe(files, tags)

    def _get_metatag_dataframe(self, paths, metatags):
        """ Reads a path or buffer and converts it into a dataframe ready for analysis """
        all_rows = []
        for path in paths:
            obj = json.load(open(path))
            rows = obj['result']
            all_rows += [ self._record_to_row(record, metatags) for record in rows ]
            
        return pd.DataFrame(all_rows, columns=metatags)

    def _record_to_row(self, record, metatags):
        """ Converts a record into a row for our dataframe """

        # Get metatags as dict
        # If key occurs more than once earlier ones are dropped
        tags = dict([(meta['name'],meta['value']) for meta in record['metatags']['metatag']])

        return tuple([tags.get(tag, None) for tag in metatags])

