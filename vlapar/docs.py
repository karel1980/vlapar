import glob
import json

if __name__=="__main__":
    totaldocs = 0
    for filename in glob.glob("*.json"):
        with open(filename) as f:
            totaldocs += len(json.load(f)['result'])

    print "There are %d docs in total"%(totaldocs)

    count = 0
    for filename in glob.glob("*.json"):
        with open(filename) as f:
            for doc in json.load(f)['result']:
                print doc['url']

