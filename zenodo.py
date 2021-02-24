import os
import requests
import json
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Retrieve Poster meta data from CS20.5 community on zenodo')
parser.add_argument('outfile',
                    help='filename for json file with query results')

args = parser.parse_args()

with open('../zenodotoken.txt') as f:
    ACCESS_TOKEN = f.read()

response = requests.get('https://zenodo.org/api/records',
                        params={'communities': 'coolstars20half',
                                #'type': 'poster',
                                'size': 1000,
                                'access_token': ACCESS_TOKEN})

for h in response.json()['hits']['hits']:
    if 'links' not in h:
        h['links'] = {}
    if 'thumbs' not in h['links']:
        h['links']['thumbs'] = {}
    if '250' not in h['links']['thumbs']:
        newthumb = 'thumbs/{}.jpg'.format(h['conceptrecid'])
        h['links']['thumbs']['250'] = newthumb
        if not os.path.exists(newthumb):
            for f in h['files']:
                if f['type'] == 'pdf':
                    r = requests.get(h['files'][0]['links']['self'],
                                     params={'access_token': ACCESS_TOKEN})
                    with open("dummy.pdf", 'wb') as f:
                         f.write(r.content)
                    break
            params = ['convert',
                      '-thumbnail', '250x250', '-background', 'transparent',
                      '-gravity', 'center', '-extent', '250x250',
                      'dummy.pdf', newthumb]
            subprocess.check_call(params)


with open(args.outfile, 'w') as f:
    json.dump(response.json(), f)
