#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Split EOMW entries.

01050890-a	cmn:lemma	悲惨的，痛苦的

->

01050890-a	cmn:lemma	悲惨的
01050890-a	cmn:lemma	痛苦的
"""

from os import listdir
from os import path
import argparse
import logging
import re

verbose = False
logger = None

separators = {',', '，'}


def init_logger(name='logger'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    log_fmt = '%(asctime)s/%(name)s[%(levelname)s]: %(message)s'
    logging.basicConfig(format=log_fmt)
    return logger


def read_tab(filepath):
    with open(filepath) as f:
        for line in f:
            row = line.split('\t')
            for sep in separators:
                if sep in row[-1]:
                    break
            for token in row[-1].split(sep):
                yield row[0], row[1], token.strip()


def main(args):
    global verbose
    verbose = args.verbose

    r_filename = re.compile(r'wn-wikt-([^\.]+).tab$')

    if verbose:
        logger.info('Read ' + args.dir_data)
    for filename in listdir(args.dir_data):
        m = r_filename.match(filename)
        if m is None:
            continue
        lang = m.group(1)
        path_input = path.join(args.dir_data, filename)
        path_output = path.join(args.dir_data, f'wn-wikt-{lang}.split.tab')
        if verbose:
            logger.info(f'in={path_input}, out={path_output}')
        with open(path_output, 'w') as f:
            for dat in read_tab(path_input):
                f.write('\t'.join(dat) + '\n')

    return 0


if __name__ == '__main__':
    logger = init_logger('Split')
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_data', default='data/wikt',
                        help='path to EOMW directory',)
    parser.add_argument('-v', '--verbose',
                        action='store_true', default=False,
                        help='verbose output')
    args = parser.parse_args()
    main(args)
