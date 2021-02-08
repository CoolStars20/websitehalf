from pagepy.abstracts import read_abstracts_table


def data(**kwargs):
    abstr = read_abstracts_table(kwargs['abstracts'], **kwargs)
    abstr = abstr[abstr['Name'] != '']
    abstr['LastName'] = [r.split(',')[0].split(' ')[-1] for r in abstr['Name']]
    abstr.sort('LastName')

    return {'participants': abstr}
