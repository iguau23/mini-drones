from __future__ import print_function

import numpy as np
import cv2 as cv2

from common import splitfn
# built-in modules
import os

if __name__ == '__main__':
    import sys
    import getopt
    from glob import glob

    args, img_mask = getopt.getopt(sys.argv[1:], '', ['debug=', 'square_size=', 'threads='])
    args = dict(args)
    args.setdefault('--debug', './output/')
    args.setdefault('--square_size', 1.0)
    args.setdefault('--threads', 4)
    if not img_mask:
        img_mask = './data_cel/foto??.jpg'  # default
    else:
        img_mask = img_mask[0]

    img_names = glob(img_mask)
    debug_dir = args.get('--debug')
    if debug_dir and not os.path.isdir(debug_dir):
        os.mkdir(debug_dir)



    for file in img_names:
        print(file)
        img = cv2.imread(file)
        resize = cv2.resize(img, (640,480), interpolation = cv2.INTER_CUBIC)
        path, name, ext = splitfn(file)
        outfile = os.path.join("./data_cel_out", name + '.jpg')
        cv2.imwrite(outfile, resize)
        print(outfile)
