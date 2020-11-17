#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import json

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

    dat = {}
    for path_input in args.path_input:
        counter = 0
        with open(path_input) as f:
            for line in f:
                entry = json.loads(line)
                entry_id = '@@@'.join([entry['token'], entry['lemma'], entry['pos']])
                if entry_id in dat:
                    dat[entry_id]['freq'] += entry['freq']
                else:
                    dat[entry_id] = entry
                counter += 1
        if verbose:
            logger.info('Read {} entries from {}'.format(counter, path_input))

    if verbose:
        logger.info('Write {} entries to {}'.format(len(dat), args.path_output))
    with open(args.path_output, 'w') as f:
        for entry in sorted(dat.values(), key=lambda item: item['freq'], reverse=True):
            f.write(json.dumps(entry) + '\n')

    return 0


if __name__ == '__main__':
    logger = init_logger('Comb')
    parser = argparse.ArgumentParser()
    parser.add_argument('path_input', help='path to input file',
                        nargs='+')
    parser.add_argument('-o', '--output', dest='path_output',
                        required=True, help='path to output file')
    parser.add_argument('-v', '--verbose',
                        action='store_true', default=False,
                        help='verbose output')
    args = parser.parse_args()
    main(args)
