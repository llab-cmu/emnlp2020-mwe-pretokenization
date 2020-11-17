#!/usr/bin/env python
# -*- coding: utf-8 -*-


from itertools import chain
import argparse
import logging
import spacy_udpipe

verbose = False
logger = None


LANGS = {'ar': 'arb',
         'de': 'deu',
         'en': 'eng',
         'es': 'spa',
         'fr': 'fra',
         'ja-unidic': 'jpn',
         'ja-ipadic': 'jpn',
         'tr': 'tur',
         'zh': 'zh-fix-simp'}


def init_logger(name='logger'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    log_fmt = '%(asctime)s/%(name)s[%(levelname)s]: %(message)s'
    logging.basicConfig(format=log_fmt)
    return logger


def setup_ja_tokenizer(dict_name):
    import MeCab
    import subprocess

    if dict_name not in ['ipadic', 'unidic']:
            logger.error('Unknown dictionary: ' + dict_name)
            raise NotImplementedError
    dir_dict = subprocess.check_output(
        'mecab-config --dicdir'.split()).strip().decode('utf_8')
    opt = ''
    if dict_name == 'unidic':
        opt += '--dicdir={}/unidic -Oipadic'.format(dir_dict)
    mecab = MeCab.Tagger(opt)
    if verbose:
        logger.info(f'MeCab: {dict_name}')
    tokenize = lambda w: [token.split('\t')[0]
                          for token in mecab.parse(w).strip().split('\n')
                          if token != 'EOS']
    return tokenize


def setup_udpipe_tokenizer(lang, path_model):
    assert args.path_model is not None
    if verbose:
        logger.info(f'Load UDPipe model: {path_model}')
    nlp = spacy_udpipe.load_from_path(lang, path_model)
    tokenize = lambda w: [token.text for token in nlp(w)]
    return tokenize


def main(args):
    global verbose
    verbose = args.verbose

    if args.lang == 'ja-ipadic':
        tokenize = setup_ja_tokenizer(args.lang.split('-')[1].lower())
    else:
        tokenize = setup_udpipe_tokenizer(args.lang, args.path_model)

    if verbose:
        logger.info('Read ' + args.path_input)
        logger.info('Write to ' + args.path_output)
    n_skipped = 0
    with open(args.path_input) as f:
        with open(args.path_output, 'w') as of:
            for i, line in enumerate(f, start=1):
                if line.startswith('#'):
                    of.write(line)
                    continue
                row = line.strip().split('\t')
                if len(row) < 3:
                    logger.warning('Skip [{}]'.format(i) + line.strip())
                    n_skipped += 1
                    continue
                tokens = tokenize(row[2])
                row[2] = '_'.join(tokens)
                of.write('\t'.join(row) + '\n')

    logger.warning('Skipped {} lines'.format(n_skipped))
    return 0


if __name__ == '__main__':
    logger = init_logger('Tokenization')
    parser = argparse.ArgumentParser()
    parser.add_argument('path_input', help='path to input file')
    parser.add_argument('--lang', required=True,
                        help='languages')
    parser.add_argument('--model', dest='path_model',
                        help='path to a model file')
    parser.add_argument('-o', '--output', dest='path_output',
                        required=True, help='path to output file')
    parser.add_argument('--port', type=int, default=9000, help='port number of StanfordCoreNLP Server')
    parser.add_argument('-v', '--verbose',
                        action='store_true', default=False,
                        help='verbose output')
    args = parser.parse_args()
    main(args)
