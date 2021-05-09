import os
import fitz
import re
import pprint

pp = pprint.PrettyPrinter(indent=2)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
IN_DATA_PATH = DIR_PATH + '\\data\\vef-1q2021.txt'
OUT_DATA_PATH = DIR_PATH + '\\data\\vef-1q2021-filtered.txt'


def contains_amount(sent):
  regex = re.compile(r'[A-Z]{3}\s-?(\d+[,\.]\d+|\d+)\s?[mln|m]')
  return re.search(regex, sent)


sents_with_amounts = []
with open(IN_DATA_PATH, 'r', encoding='utf8') as f:
  lines = f.readlines()
  for sent in lines:
    if contains_amount(sent):
      sents_with_amounts.append(sent)

with open(OUT_DATA_PATH, 'w', encoding='utf8') as f:
  for sent in sents_with_amounts:
    f.write(sent)
