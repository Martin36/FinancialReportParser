import nltk
import os
from nltk.tokenize import word_tokenize
import pprint

nltk.download('averaged_perceptron_tagger')

pp = pprint.PrettyPrinter(indent=2)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = DIR_PATH + '\data\interim-report-Q42020-filtered.txt'


def grammar_parser(f):
  num_grammar = "NUM: {<NNP>?<CD>}"
  num_parser = nltk.RegexpParser(num_grammar)
  # sub_grammar = r"""
  #   NP:
  #     {<DT>?<JJ.*>*<NN.*>+}
  #   """
  # sub_grammar = r"""
  #   NP:
  #     {<.*>+}          # Chunk everything
  #     }<VB.*|NUM>+{
  # """
  sub_grammar = r"""
    NP: 
      {<DT|JJ|NN.*>+<IN|CC>?<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
      {<DT|JJ|NN.*>+}
      }<VB.*|NUM>+{
    VP:
      {<VB.*><NP|NUM>}
    OF:
      {<IN><NUM>}
    REL:
      {<NP><VP|OF><NP>?}
  """
  sub_parser = nltk.RegexpParser(sub_grammar)
  concat_grammar = "NP: {<NP><IN><NP>}"
  concat_parser = nltk.RegexpParser(concat_grammar)
  sents = f.readlines()

  for i, sent in enumerate(sents[:5]):
    text = word_tokenize(sent)
    tagged_text = nltk.pos_tag(text)
    parsed_text = num_parser.parse(tagged_text)
    parsed_text = sub_parser.parse(parsed_text)
    parsed_text = concat_parser.parse(parsed_text)
    print(parsed_text)
    # if i == 0:
    #   parsed_text.draw()


def nltk_ne_chunker(f):
  nltk.download('treebank')
  nltk.download('maxent_ne_chunker')
  nltk.download('words')

  sents = f.readlines()
  for _, sent in enumerate(sents[:5]):
    text = word_tokenize(sent)
    tagged_text = nltk.pos_tag(text)
    print(sent)
    print(nltk.ne_chunk(tagged_text, binary=True))


with open(DATA_PATH, 'r', encoding='utf8') as f:
  nltk_ne_chunker(f)
