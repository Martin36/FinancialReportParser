import re
import pprint
from openie import StanfordOpenIE

pp = pprint.PrettyPrinter(indent=2)
text_file = open("input_text.txt", "r", encoding="utf8")

with StanfordOpenIE() as client:
  text = text_file.read().replace('\n', ' ').replace('\r', '')
  # print('Text: %s.' % text)
  relations = []
  for triple in client.annotate(text):
    relations.append(triple)
    print('|-', triple)

  # Filter the results to only include objects consisting of numbers
  relations = [rel for rel in relations if re.search(r'SEK -?.*\d+m', rel['object'])]
  pp.pprint(relations)

  # This code returns the whole thing that CoreNLP does
  # res = client.annotate(text, simple_format=False)
  # pp.pprint(res)

  # TODO: Find duplicates and merge them


text_file.close()