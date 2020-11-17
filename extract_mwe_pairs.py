#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Build a bilingual dictionarie with MWE entries.

(Assume wn-wikt-*.tab files are in ./wikt/ and we write a resulting dictionary to wikt/mwe-dict)
python extract_mwe_pairs.py --src en --tgt es -o wikt/mwe-dict/ -v


usage: extract_mwe_pairs.py [-h] [--dir DIR_WIKT] [--src SRC] --tgt TGT [-o DIR_OUTPUT]
                            [--src-port SRC_PORT] [--tgt-port TGT_PORT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  --dir DIR_WIKT        path to a data directory
  --src SRC             source language
  --tgt TGT             target language
  -o DIR_OUTPUT, --output DIR_OUTPUT
                        path to an output directory
  --src-port SRC_PORT
  --tgt-port TGT_PORT
  -v, --verbose         verbose output
"""

from collections import defaultdict
from os import path
import argparse
import csv
import logging

LANGS = {'ar': 'arb',
         'bg': 'bul',
         'de': 'deu',
         'en': 'eng',
         'es': 'spa',
         'fr': 'fra',
         'he': 'heb',
         'hi': 'hin',
         'ja-unidic': 'jpn-unidic',
         'ja-ipadic': 'jpn-ipadic',
         'ru': 'rus',
         'tr': 'tur',
         'zh': 'cmn-simp'}

def init_logger(name='logger'):
    """Initialize a logger"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    log_fmt = '%(asctime)s/%(name)s[%(levelname)s]: %(message)s'
    logging.basicConfig(format=log_fmt)
    return logger

logger = init_logger('MWEDict')

parser = argparse.ArgumentParser()
parser.add_argument('--dir', dest='dir_wikt', default='data/wikt',
                    help='path to a data directory')
parser.add_argument('--src', default='en',
                    help='source language')
parser.add_argument('--tgt', required=True, help='target language')
parser.add_argument('-o', '--output', dest='dir_output', default='.',
                    help='path to an output directory')
parser.add_argument('--src-port', type=int, default=9000)
parser.add_argument('--tgt-port', type=int, default=10000)
parser.add_argument('-v', '--verbose',
                    action='store_true', default=False,
                    help='verbose output')
args = parser.parse_args()
verbose = args.verbose

# source language
path_src = path.join(args.dir_wikt,
                     'wn-wikt-{}.split.tkn.tab'.format(LANGS[args.src]))
# target langauge
path_tgt = path.join(args.dir_wikt,
                     'wn-wikt-{}.split.tkn.tab'.format(LANGS[args.tgt]))

src_tab = list()
tgt_tab = list()


# Read lexicon
src_lex = defaultdict(set)  # SynsetID (str) -> words (set)
tgt_lex = defaultdict(set)

if verbose:
    logger.info('SRC: ' + path_src)
    logger.info('TGT: ' + path_tgt)
with open(path_src, 'r') as f:
    next(f) # skip headings
    reader = csv.reader(f, delimiter='\t')
    for synset, _, word in reader:
        if len(word) == 1:  # ignore one-char words
            continue
        src_lex[synset].add(word.lower())

with open(path_tgt, 'r') as f:
    next(f) # skip headings
    reader = csv.reader(f, delimiter='\t')
    for synset, _, word in reader:
        if len(word) == 1:  # ignore one-char words
            continue
        tgt_lex[synset].add(word.lower())

## Sort for the consistency (set -> list)
for synset in src_lex:
    src_lex[synset] = sorted(list(src_lex[synset]))
for synset in tgt_lex:
    tgt_lex[synset] = sorted(list(tgt_lex[synset]))


# Get a list of SynsetIDs that exist in the both languages
synset_shared = set(src_lex.keys()).intersection(tgt_lex.keys())
if verbose:
    logger.info('{} shared synsets'.format(len(synset_shared)))


# Output
path_output = path.join(args.dir_output,
                        '{}-{}.mwe.txt'.format(args.src, args.tgt))
counter = 0
if verbose:
    logger.info('Output: ' + path_output)
with open(path_output, 'w') as f:
    for synset in sorted(list(synset_shared)):
        for src_word in src_lex[synset]:
            # Ignore translations between single-token source words
            if len(src_word.split('_')) == 1:
                continue
            for tgt_word in tgt_lex[synset]:
                f.write(src_word + ' ' + tgt_word + '\n')
                counter += 1
if verbose:
    logger.info('Wrote {} entries'.format(counter))
