from stanza.server import CoreNLPClient
import os
import re

os.environ["CORENLP_HOME"] = "C:\\Program Files\\stanford-corenlp-4.2.0"
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = DIR_PATH + '\\input.txt'

with open(DATA_PATH, 'r') as f:
  text = f.readlines()
  text = " ".join(text)
  text = text.replace('\n', '')

# set up the client
print('---')
print('starting up Java Stanford CoreNLP Server...')

# set up the client
with CoreNLPClient(annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'depparse', 'coref'], timeout=60000, memory='16G') as client:
  # submit the request to the server
  ann = client.annotate(text)

  # get the first sentence
  sentence = ann.sentence[0]

  subj_pattern = '{} <<nsubj {}'
  obj_regex = re.compile(r'[A-Z]{3}\s-?\d+(,\d+)?m')
  matches = client.semgrex(text, subj_pattern)
  relations = []
  for sent in matches['sentences']:
    rel_obj = {}
    word_list = []
    for key in sent:
      if key != 'length':
        word_list.append(sent[key])
    word_list = sorted(word_list, key=lambda i: i['begin'])
    subj = " ".join([word['text'] for word in word_list])
    rel_obj['subject'] = subj
    relations.append(rel_obj)
    print(subj)
  print(relations)

client.stop()
