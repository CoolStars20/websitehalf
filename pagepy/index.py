from glob import glob
import csv

def data(**kwargs):

    images = glob('images/slide-*')
    images.sort()

    return {'images': images}
