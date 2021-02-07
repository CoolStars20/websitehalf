import json
from fuzzywuzzy import process


def data(**kwargs):
    major_science_topics = [
        'The Sun and the Heliosphere',
        'Very low mass stars',
        'Post main sequence cool stars',
        'Young stars',
        'Cool Stars on the main sequence',
        'Stellar systems, clusters, and associations']

    posters = {m: [] for m in major_science_topics}
    posters['Other'] = []

    with open(kwargs['zenodoposter']) as f:
        zenodo = json.load(f)

    for h in zenodo['hits']['hits']:
        keylist = h['metadata']['keywords']
        topic = 'Other'
        for k in reversed(keylist):
            matched = process.extractOne(k, major_science_topics)
            if matched[1] > 95:
                topic = matched[0]

        posters[topic].append(h)

    # Within each category, sort posters by creation time
    for v in posters.values():
        v.sort(key=lambda h: h['created'])

    return {'posters': posters}
