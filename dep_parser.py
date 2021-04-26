import os
import pprint
from nltk.parse.stanford import StanfordDependencyParser

pp = pprint.PrettyPrinter(indent=2)

path_to_jar = 'C:\\Program Files\\stanford-parser-4.2.0\\stanford-parser-full-2020-11-17\\stanford-parser.jar'
path_to_models_jar = 'C:\\Program Files\\stanford-parser-4.2.0\\stanford-parser-full-2020-11-17\\stanford-parser-4.2.0-models.jar'

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = DIR_PATH + '\\input.txt'


dependency_parser = StanfordDependencyParser(
    path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

with open(DATA_PATH, 'r', encoding='utf8') as f:
  text = f.readline()
  result = dependency_parser.raw_parse(text)
  dep = result.__next__()

  # triples = list(dep.triples())
  triples = dep.triples()
  dep_tree = dep.tree()
  subject = {
      'nsubj': '',
      'nmod': '',
      'obj': ''
  }
  for node in dep_tree:
    print(node)
  for triple in triples:
    print(triple)
    if triple[1] == 'nsubj':
      (word, pos) = triple[2]
      subject['nsubj'] += word
    elif triple[1] == 'nmod':
      (word, pos) = triple[2]
      subject['nmod'] += word

    # dep.tree().draw()
