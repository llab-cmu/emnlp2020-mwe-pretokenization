# Pre-tokenization of Multi-word Expressions in Cross-lingualWord Embeddings

This repository contains the data and code created in our work "[Pre-tokenization of Multi-word Expressions in Cross-lingualWord Embeddings](https://www.aclweb.org/anthology/2020.emnlp-main.360/)".


## Scripts for building MWE lexicons

We describe below how to build (1) MWE lists that are used for identifying MWEs in texts and (2) bilingual dictionaries that are used for evaluate cross-lingual mappings of MWEs. The same method can be easily applied to language pairs that are not covered in our paper (e.g., en-fr).

### Dependencies

- [OpenCC](https://github.com/BYVoid/OpenCC) (for converting Chinese characters; follow the instruction to install OpenCC)
- Python libraries: `spacy-udpipe`, `mecab-python3` (for tokenizing texts. `mecab` for Japanese)

```shell
pip install spacy-udpipe
pip install mecab-python3
```

Download and place [CoNLL17 Shared Task Baseline UD 2.0 Models (`udpipe-ud2.0-conll17-170315`)](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-1990) under `udpipe_models/`.

## Download and pre-processing

Download [Extended Open Multilingual WordNet](http://compling.hss.ntu.edu.sg/omw/summx.html).

```shell
wget http://compling.hss.ntu.edu.sg/omw/wn-wikt.tar.bz2
tar xfv wn-wikt.tar.bz2 data/wikt
rm wn-wikt.tar.bz2

# Split lexical (Some lines contains two or more lexical units)
python split_eomw_entry.py data/wikt/ -v

# Convert Chinese data into traditional characters
opencc -c s2t.json < data/wikt/wn-wikt-cmn.split.tab > data/wikt/wn-wikt-cmn-trad.split.tab
```

## (1) Extract an MWE list for each language

Extract MWE entries and save them in JSON format.

### Extended Open Multilingual Wordnet (EOMW)

```shell
python wnwikt2json_udpipe.py data/wikt/wn-wikt-arb.split.tab -o data/mwelex/ar-eomw.v1.json --model udpipe_models/arabic-ud-2.0-conll17-170315.udpipe --lang ar -v
python wnwikt2json_udpipe.py data/wikt/wn-wikt-bul.split.tab -o data/mwelex/bg-eomw.v1.json --model udpipe_models/bulgarian-ud-2.0-conll17-170315.udpipe --lang bg -v
python wnwikt2json_udpipe.py data/wikt/wn-wikt-deu.split.tab -o data/mwelex/de-eomw.v1.json --model udpipe_models/german-ud-2.0-conll17-170315.udpipe --lang de -v
python wnwikt2json_udpipe.py data/wikt/wn-wikt-eng.split.tab -o data/mwelex/en-eomw.v1.json --model udpipe_models/english-ud-2.0-conll17-170315.udpipe --lang en -v
python wnwikt2json_udpipe.py data/wikt/wn-wikt-heb.split.tab -o data/mwelex/he-eomw.v1.json --model udpipe_models/hebrew-ud-2.0-conll17-170315.udpipe --lang he -v
python wnwikt2json_udpipe.py data/wikt/wn-wikt-hin.split.tab -o data/mwelex/hi-eomw.v1.json --model udpipe_models/hindi-ud-2.0-conll17-170315.udpipe --lang hi -v
python wnwikt2json_udpipe.py data/wikt/wn-wikt-rus.split.tab -o data/mwelex/ru-eomw.v1.json --model udpipe_models/russian-ud-2.0-conll17-170315.udpipe --lang ru -v
python wnwikt2json_udpipe.py data/wikt/wn-wikt-spa.split.tab -o data/mwelex/es-eomw.v1.json --model udpipe_models/spanish-ud-2.0-conll17-170315.udpipe --lang es -v
python wnwikt2json_udpipe.py data/wikt/wn-wikt-tur.split.tab -o data/mwelex/tr-eomw.v1.json --model udpipe_models/turkish-ud-2.0-conll17-170315.udpipe --lang en -v

# Japanese (UNIDIC and IPADIC)
python wnwikt2json_udpipe.py data/wikt/wn-wikt-jpn.split.tab -o data/mwelex/ja-unidic-eomw.v1.json --model udpipe_models/japanese-ud-2.0-conll17-170315.udpipe --lang ja -v
python wnwikt2json_mecab.py data/wikt/wn-wikt-jpn.split.tab -o data/mwelex/ja-ipadic-eomw.v1.json --dict ipadic -v

# Chinese
python wnwikt2json_udpipe.py data/wikt/wn-wikt-cmn-trad.split.tab -o data/mwelex/zh-trad-eomw.v1.json --model udpipe_models/chinese-ud-2.0-conll17-170315.udpipe --lang zh -v
opencc -c t2s.json < data/mwelex/zh-trad-eomw.v1.json > data/mwelex/zh-eomw.v1.json
```

Convert them into XML (mwetoolkit3 format)

```shell

# EOMW
python json2xml.py data/mwelex/ar-eomw.v1.json -o data/mwelex/ar-eomw.v1.xml -v
python json2xml.py data/mwelex/bg-eomw.v1.json -o data/mwelex/bg-eomw.v1.xml -v
python json2xml.py data/mwelex/de-eomw.v1.json -o data/mwelex/de-eomw.v1.xml -v
python json2xml.py data/mwelex/en-eomw.v1.json -o data/mwelex/en-eomw.v1.xml -v
python json2xml.py data/mwelex/es-eomw.v1.json -o data/mwelex/es-eomw.v1.xml -v
python json2xml.py data/mwelex/he-eomw.v1.json -o data/mwelex/he-eomw.v1.xml -v
python json2xml.py data/mwelex/hi-eomw.v1.json -o data/mwelex/hi-eomw.v1.xml -v
python json2xml.py data/mwelex/ja-ipadic-eomw.v1.json -o data/mwelex/ja-ipadic-eomw.v1.xml -v
python json2xml.py data/mwelex/ja-unidic-eomw.v1.json -o data/mwelex/ja-unidic-eomw.v1.xml -v
python json2xml.py data/mwelex/tr-eomw.v1.json -o data/mwelex/tr-eomw.v1.xml -v
python json2xml.py data/mwelex/ru-eomw.v1.json -o data/mwelex/ru-eomw.v1.xml -v
python json2xml.py data/mwelex/zh-eomw.v1.json -o data/mwelex/zh-eomw.v1.xml -v
```


### PARSEME v1.1

__v1: from PARSEME annotations__

```shell
python cupt2json.py mwe-lexicon/PARSEME/BG/{train,dev,test}.cupt -o data/mwelex/bg-parseme.v1.json --source PARSEMEv1.1 -v
python cupt2json.py mwe-lexicon/PARSEME/DE/{train,dev,test}.cupt -o data/mwelex/de-parseme.v1.json --source PARSEMEv1.1 -v
python cupt2json.py mwe-lexicon/PARSEME/EN/{train,test}.cupt -o data/mwelex/en-parseme.v1.json --source PARSEMEv1.1 -v
python cupt2json.py mwe-lexicon/PARSEME/ES/{train,dev,test}.cupt -o data/mwelex/es-parseme.v1.json --source PARSEMEv1.1 -v
python cupt2json.py mwe-lexicon/PARSEME/HI/{train,test}.cupt -o data/mwelex/hi-parseme.v1.json --source PARSEMEv1.1 -v
python cupt2json.py mwe-lexicon/PARSEME/HE/{train,dev,test}.cupt -o data/mwelex/he-parseme.v1.json --source PARSEMEv1.1 -v
python cupt2json.py mwe-lexicon/PARSEME/TR/{train,dev,test}.cupt -o data/mwelex/tr-parseme.v1.json --source PARSEMEv1.1 -v
```

### Combine parseme with eomw

```shell
python json2xml.py data/mwelex/bg-{eomw,parseme}.v1.json -o data/mwelex/bg-eomw+parseme.v1.xml -v
python json2xml.py data/mwelex/de-{eomw,parseme}.v1.json -o data/mwelex/de-eomw+parseme.v1.xml -v
python json2xml.py data/mwelex/en-{eomw,parseme}.v1.json -o data/mwelex/en-eomw+parseme.v1.xml -v
python json2xml.py data/mwelex/es-{eomw,parseme}.v1.json -o data/mwelex/es-eomw+parseme.v1.xml -v
python json2xml.py data/mwelex/he-{eomw,parseme}.v1.json -o data/mwelex/he-eomw+parseme.v1.xml -v
python json2xml.py data/mwelex/hi-{eomw,parseme}.v1.json -o data/mwelex/hi-eomw+parseme.v1.xml -v
python json2xml.py data/mwelex/tr-{eomw,parseme}.v1.json -o data/mwelex/tr-eomw+parseme.v1.xml -v
```


### Stats

language|eomw|eomw+parseme|
:-------|---:|-----------:|
ar      |1608||
bg      |1022|3255|
da      |412||
de      |1097|2705|
en      |8552|8982|
es      |3079|4485|
fr      |3600|5609
he      |934|2454|
ja-unidic|3897
ja-ipadic|5006
tr      |1959|4240|
zh      |6927


## (2) Pair MWE entries by synset identifiers

### Tokenize lexicons


```shell
python tokenize_wn-wikt.py data/wikt/wn-wikt-arb.split.tab -o data/wikt/wn-wikt-arb.split.tkn.tab --lang ar --model udpipe_models/arabic-ud-2.0-conll17-170315.udpipe -v
python tokenize_wn-wikt.py data/wikt/wn-wikt-bul.split.tab -o data/wikt/wn-wikt-bul.split.tkn.tab --lang bg --model udpipe_models/bulgarian-ud-2.0-conll17-170315.udpipe -v
python tokenize_wn-wikt.py data/wikt/wn-wikt-deu.split.tab -o data/wikt/wn-wikt-deu.split.tkn.tab --lang de --model udpipe_models/german-ud-2.0-conll17-170315.udpipe -v
python tokenize_wn-wikt.py data/wikt/wn-wikt-eng.split.tab -o data/wikt/wn-wikt-eng.split.tkn.tab --lang en --model udpipe_models/english-ud-2.0-conll17-170315.udpipe -v
python tokenize_wn-wikt.py data/wikt/wn-wikt-heb.split.tab -o data/wikt/wn-wikt-heb.split.tkn.tab --lang he --model udpipe_models/hebrew-ud-2.0-conll17-170315.udpipe -v
python tokenize_wn-wikt.py data/wikt/wn-wikt-hin.split.tab -o data/wikt/wn-wikt-hin.split.tkn.tab --lang hi --model udpipe_models/hindi-ud-2.0-conll17-170315.udpipe -v
python tokenize_wn-wikt.py data/wikt/wn-wikt-rus.split.tab -o data/wikt/wn-wikt-rus.split.tkn.tab --lang ru --model udpipe_models/russian-ud-2.0-conll17-170315.udpipe -v
python tokenize_wn-wikt.py data/wikt/wn-wikt-spa.split.tab -o data/wikt/wn-wikt-spa.split.tkn.tab --lang es --model udpipe_models/spanish-ud-2.0-conll17-170315.udpipe -v
python tokenize_wn-wikt.py data/wikt/wn-wikt-tur.split.tab -o data/wikt/wn-wikt-tur.split.tkn.tab --lang tr --model udpipe_models/turkish-ud-2.0-conll17-170315.udpipe -v

# Japanese (UNIDIC and IPADIC)
python tokenize_wn-wikt.py data/wikt/wn-wikt-jpn.split.tab -o data/wikt/wn-wikt-jpn-unidic.split.tkn.tab --lang ja --model udpipe_models/japanese-ud-2.0-conll17-170315.udpipe -v
python tokenize_wn-wikt.py data/wikt/wn-wikt-jpn.split.tab -o data/wikt/wn-wikt-jpn-ipadic.split.tkn.tab --lang ja-ipadic -v
# python tokenize_wn-wikt.py data/wikt/wn-wikt-jpn.split.tab -o data/wikt/wn-wikt-jpn-ipadic.tkn.tab --lang ja-uniadic -v

# Chinese (We tokenize traditional characters with UDPipe and convert them into simplified)
python tokenize_wn-wikt.py data/wikt/wn-wikt-cmn-trad.split.tab -o data/wikt/wn-wikt-cmn-trad.split.tkn.tab --lang zh --model udpipe_models/chinese-ud-2.0-conll17-170315.udpipe -v
opencc -c t2s.json < data/wikt/wn-wikt-cmn-trad.split.tkn.tab > data/wikt/wn-wikt-cmn-simp.split.tkn.tab
```


### Obtain bilingual word pairs

```shell
# from en to L2
python extract_mwe_pairs.py --src en --tgt ar -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --src en --tgt bg -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --src en --tgt de -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --src en --tgt es -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --src en --tgt he -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --src en --tgt hi -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --src en --tgt ja-ipadic -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --src en --tgt ja-unidic -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --src en --tgt ru -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --src en --tgt tr -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --src en --tgt zh -o data/wikt/mwe-dict/ -v

# from L2 to en
python extract_mwe_pairs.py --tgt en --src ar -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --tgt en --src bg -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --tgt en --src de -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --tgt en --src es -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --tgt en --src he -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --tgt en --src hi -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --tgt en --src ja-ipadic -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --tgt en --src ja-unidic -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --tgt en --src ru -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --tgt en --src tr -o data/wikt/mwe-dict/ -v
python extract_mwe_pairs.py --tgt en --src zh -o data/wikt/mwe-dict/ -v
```
