#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from itertools import chain
from tqdm import tqdm
import subprocess
import MeCab
import argparse
import logging
import pandas as pd

from utils import write_mwe_json

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

    df = pd.read_table(args.path_input, names=['synset', 'type', 'surface'],
                       comment='#')
    df.dropna(inplace=True)
    if verbose:
        logger.info('Read {} lines from {}'.format(len(df), args.path_input))
    words = sorted(df['surface'].unique())

    if verbose:
        logger.info('# of words: ' + str(len(words)))

    # Set up MeCab
    if verbose:
        logger.info('MeCab: {}'.format(args.dict))
    dir_dict = subprocess.check_output('mecab-config --dicdir'.split()).strip().decode('utf_8')
    opt = ''
    if args.dict == 'unidic':
        opt += '--dicdir={}/unidic -Oipadic'.format(dir_dict)
    mecab = MeCab.Tagger(opt)

    counter = defaultdict(int)
    for word in tqdm(words):
        buff = []
        for token in mecab.parse(word).split('\n'):
            try:
                form, feats = token.split('\t', 1)
            except ValueError:
                continue
            feats = feats.split(',')
            pos = feats[0]
            if len(feats) == 9:
                lemma = feats[6]
            else:
                lemma = form
            if form in ['～', '…']:  # skip symbols
                continue
            buff.append('@@@'.join([form, lemma, pos]))

        if len(buff) == 1:
            continue
        counter['\t'.join(buff)] += 1


    if verbose:
        logger.info('Write {} entries to {}'.format(len(counter), args.path_output))
    write_mwe_json(args.path_output, counter, source='EOMW')

    return 0


if __name__ == '__main__':
    logger = init_logger('MWE')
    parser = argparse.ArgumentParser()
    parser.add_argument('path_input', help='path to input file')
    parser.add_argument('--dict', choices=['ipadic', 'unidic'], default='ipadic',
                        help='MeCab dictionary')
    parser.add_argument('-o', '--output', dest='path_output',
                        required=True, help='path to output file')
    parser.add_argument('-v', '--verbose',
                        action='store_true', default=False,
                        help='verbose output')
    args = parser.parse_args()
    main(args)
