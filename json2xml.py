#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import argparse
import json
import logging

from utils import write_json2xml
from utils import escape

verbose = False
logger = None


def init_logger(name='logger'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    log_fmt = '%(asctime)s/%(name)s[%(levelname)s]: %(message)s'
    logging.basicConfig(format=log_fmt)
    return logger


def main(args):
    global verbose
    verbose = args.verbose

    if verbose:
        logger.info('Read ' + args.col)
    mwes = {}
    counts = 0
    for filename in args.path_input:
        if verbose:
            logger.info('Read ' + filename)
        with open(filename) as f:
            for n_lines, line in enumerate(f, start=1):
                dat = json.loads(line)
                dat[args.col] = escape(dat[args.col])
                if dat[args.col] in mwes:
                    mwes[dat[args.col]]['freq'].append((dat['source'], dat['freq']))
                    continue
                mwes[dat[args.col]] = dat
                freq = (mwes[dat[args.col]]['source'], mwes[dat[args.col]]['freq'])
                mwes[dat[args.col]]['freq'] = [freq]
                del mwes[dat[args.col]]['source']
            counts += n_lines

    if verbose:
        logger.info('Read {} entries'.format(counts))
        logger.info('Write {} entries to {}'.format(len(mwes), args.path_output))
    write_json2xml(args.path_output, mwes)
    return 0


if __name__ == '__main__':
    logger = init_logger('json2xml')
    parser = argparse.ArgumentParser()
    parser.add_argument('path_input', nargs='+', help='path to input file',)
    parser.add_argument('-o', '--output', dest='path_output',
                        help='path to output file')
    parser.add_argument('--col', choices=['lemma'], default='lemma')
    parser.add_argument('-v', '--verbose',
                        action='store_true', default=False,
                        help='verbose output')
    args = parser.parse_args()
    main(args)
