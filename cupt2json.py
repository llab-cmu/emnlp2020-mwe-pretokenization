#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract MWEs from cupt format and save them in JSON format
"""

from collections import defaultdict
from tqdm import tqdm
import argparse
import codecs
import json
import logging

verbose = False
logger = None


def init_logger(name='logger'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    log_fmt = '%(asctime)s/%(name)s[%(levelname)s]: %(message)s'
    logging.basicConfig(format=log_fmt)
    return logger


def write_mwe_json(filename, mwes, types, source='n/a'):
    with codecs.open(filename, 'w', encoding='utf_8') as f:
        for mwe, freq in sorted(mwes.items(), key=lambda t: t[1], reverse=True):
            token, lemma, upos = zip(*[entry.split('@@@') for entry in mwe.split('\t')])
            row = {'token': ' '.join(token),
                   'lemma': ' '.join(lemma),
                   'pos': ' '.join(upos),
                   'parseme_tag': ' '.join(sorted(list(set(types[mwe])))),
                   'freq': freq,
                   'source': source}
            f.write(json.dumps(row, ensure_ascii=False) + '\n')


def read_cupt(filename):
    """Read a file in CoNLL format and yield mwes"""

    if verbose:
        logger.info('Read ' + filename)

    tokens = []
    mwes = defaultdict(list)
    mwe_types = {}
    with codecs.open(filename, encoding='utf_8') as f:
        for line in tqdm(f):
            line = line.strip()
            if len(line) == 0:
                yield mwes, mwe_types
                tokens = []
                mwes = defaultdict(list)
                mwe_types = {}
                continue
            if line.startswith('#'):
                continue
            token = line.split('\t')
            tokens.append(token)
            if token[-1] == '*':  # not in an MWE
                continue
            for tag in token[-1].split(';'):
                mwe_id = int(tag.split(':')[0])
                mwes[mwe_id].append(token)
                try:
                    mwe_type = tag.split(':')[1]
                    mwe_types[mwe_id] = mwe_type
                except IndexError:
                    pass
                if len(mwes[mwe_id]) > 1:
                    idx1, idx2 = int(mwes[mwe_id][-1][0]), int(mwes[mwe_id][-2][0])
                    if idx1 - idx2  == 2:
                        if tokens[idx1 - 2][3] == 'DET':  # insert a determinor
                            mwes[mwe_id].insert(-1, tokens[idx1 - 2])

    if len(mwes) > 0:
        yield mwes, mwe_types


def main(args):
    global verbose
    verbose = args.verbose

    counter = defaultdict(int)
    types = defaultdict(list)

    for path_input in args.path_input:
        for mwes, mwe_types in read_cupt(path_input):
            for mwe_id, tokens in mwes.items():
                buff = []
                for token in tokens:
                    form, lemma, upos = token[1], token[2], f'{token[3]}-{token[4]}'
                    if not isinstance(form, str) \
                       and not isinstance(lemma, str):
                        buff =[]  # invalid entry. skip.
                        break
                    if not isinstance(form, str):
                        form = lemma
                    if not isinstance(lemma, str):
                        lemma = form
                    entry = ['{}'.format(form),
                             '{}'.format(lemma.lower()),
                             '{}'.format(upos)]
                    buff.append('@@@'.join(entry))
                if len(buff) <= 1:
                    continue
                counter['\t'.join(buff)] += 1
                types['\t'.join(buff)].append(mwe_types[mwe_id])

    if verbose:
        logger.info('Write {} entries to {}'.format(len(counter), args.path_output))
        logger.info('Total count: {}'.format(sum(counter.values())))
    write_mwe_json(args.path_output, counter, types, source=args.source)

    return 0



if __name__ == '__main__':
    logger = init_logger('MWE[CUPT]')
    parser = argparse.ArgumentParser()
    parser.add_argument('path_input', nargs='+', help='path to input file')
    parser.add_argument('-s', '--source', default='n/a',
                        help='data source')
    parser.add_argument('-o', '--output', dest='path_output',
                        help='path to output file')
    parser.add_argument('-v', '--verbose',
                        action='store_true', default=False,
                        help='verbose output')
    args = parser.parse_args()
    main(args)
