import codecs
import json


def escape(s):
    """Escape special characters for mwetoolkit formats."""
    if not isinstance(s, str):
        return s
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('"', '&quot;')
    s = s.replace('\t', '&#9;')
    s = s.replace('\n', '&#10;')
    return s

def write_json2xml(filename, mwes):
    with open(filename, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<!DOCTYPE dict SYSTEM "dtd/mwetoolkit-dict.dtd">\n'
                '<!-- MWETOOLKIT: filetype="XML" -->\n'
                '<dict>\n'
                '<meta></meta>\n\n')
        for mwe, entry in sorted(mwes.items(), key=lambda t: t[0]):
            f.write('<entry>\n')
            for item in mwe.split(' '):
                f.write(' ' * 8 + '<w lemma="{}" />\n'.format(item))
            f.write('</entry>\n\n')
        f.write('</dict>\n')


def write_mwe_json(filename, mwes, source='n/a'):
    with codecs.open(filename, 'w', encoding='utf_8') as f:
        for mwe, freq in sorted(mwes.items(), key=lambda t: t[1], reverse=True):
            try:
                token, lemma, upos, ner = zip(*[entry.split('@@@') for entry in mwe.split('\t')])
            except:
                token, lemma, upos = zip(*[entry.split('@@@') for entry in mwe.split('\t')])
            row = {'token': ' '.join(token),
                   'lemma': ' '.join(lemma),
                   'pos': ' '.join(upos)}
            try:
                row['ner'] = ' '.join(ner)
            except:
                pass
            row['freq'] = freq
            row['source'] = source
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
