from stanza.server import CoreNLPClient
import os
import re
import json
import pprint

pp = pprint.PrettyPrinter(indent=2)

os.environ["CORENLP_HOME"] = "C:\\Program Files\\stanford-corenlp-4.2.0"
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = DIR_PATH + '\\data\\interim-report-Q42020-filtered.txt'

with open(DATA_PATH, 'r', encoding='utf-8') as f:
  text = f.readlines()
  text = " ".join(text)
  text = text.replace('\n', '')
  # Replace all the uccurances of a digit followed by "m.", since this may be wrongly asserted to be an abbrivation for the parser
  text = re.sub(r'(\d)(m\.)', r'\1m .', text)


def filter_words(word_list):
  result = []
  for i, word in enumerate(word_list):
    if i == 0:
      result.append(word)
    elif word['text'] != word_list[i-1]['text']:
      result.append(word)
  return result


def get_only_consecutive_words(word_list):
  result = []
  for i, word in enumerate(word_list):
    if i != 0 and word['begin'] != word_list[i-1]['end']:
      break
    result.append(word)
  return result


  # set up the client
print('---')
print('starting up Java Stanford CoreNLP Server...')

# set up the client
with CoreNLPClient(annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'depparse', 'coref'],
                   timeout=60000, memory='16G', endpoint="http://localhost:9001") as client:
  # submit the request to the server
  ann = client.annotate(text)

  org_sents = []
  for sentence in ann.sentence:
    org_sent = ""
    for token in sentence.token:
      org_sent += token.originalText + " "
    org_sents.append(org_sent.strip())

  subj_pattern = '{} <<nsubj {} | >acl {} | </amod|case/ ({} >acl {}) | >/nmod.*/ ({} >acl {})'
  obj_regex = re.compile(r'[A-Z]{3}\s-?\d+(,\d+)?m')
  matches = client.semgrex(text, subj_pattern)
  relations = []
  for i, sent in enumerate(matches['sentences']):
    rel_obj = {}
    rel_obj['org_sent'] = org_sents[i]
    word_list = []
    for key in sent:
      if key != 'length':
        word_list.append(sent[key])
    word_list = sorted(word_list, key=lambda i: i['begin'])
    word_list = filter_words(word_list)
    # split when the words are no longer consecutive
    word_list = get_only_consecutive_words(word_list)
    subj = " ".join([word['text'] for word in word_list])
    rel_obj['subject'] = subj
    relations.append(rel_obj)
    print(subj)

  matches = client.tokensregex(
      text, '/[A-Z]{3}/ /-?[0-9]{1,3}(,[0-9]{3})?m?/ /m/?')
  for i, sent in enumerate(matches['sentences']):
    if '0' in sent:
      obj = sent['0']['text']
      relations[i]['object'] = obj

  # relations = [relation for relation in relations if 'object' in relation]

  pp.pprint(relations)

  outFile = open("relations.json", "w")
  outFile.write(json.dumps(relations, indent=2))
  outFile.close()


client.stop()
