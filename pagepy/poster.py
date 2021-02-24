import json
from fuzzywuzzy import process
from astropy.table import Table


def data(**kwargs):
    major_science_topics = [
        'Interactive Posters',
        'The Sun and the Heliosphere',
        'Very low mass stars',
        'Post main sequence cool stars',
        'Young stars',
        'Cool Stars on the main sequence',
        'Stellar systems, clusters, and associations']

    posters = {m: [] for m in major_science_topics}
    posters['Other'] = []
    posterlinks = []

    with open(kwargs['zenodoposter']) as f:
        zenodo = json.load(f)

    for h in zenodo['hits']['hits']:
        topic = 'Other'
        # If they did not set any keywords, we'll just put it in "other"
        if 'keywords' in h['metadata']:
            keylist = h['metadata']['keywords']

            for k in reversed(keylist):
                matched = process.extractOne(k, major_science_topics)
                if matched[1] > 95:
                    topic = matched[0]

        for f in h['files']:
            # Check if there is at least one pdf
            # if not, this might be a haiku upload
            if f['type'] == 'pdf':
                posters[topic].append(h)
                posterlinks.append(h['links']['html'])
                break

    # Within each category, sort posters by creation time
    for v in posters.values():
        v.sort(key=lambda h: h['created'])

    interactive = Table.read('data/interactive_poststers.csv',
                             format='ascii')
    posters['Interactive Posters'] = interactive
    for row in interactive:
        posterlinks.append(row['html'])

    with open('data/posterlinks.json', 'w') as fp:
        json.dump(posterlinks, fp)

    return {'posters': posters}
