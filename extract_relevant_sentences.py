import os
import fitz
import re
import pprint

pp = pprint.PrettyPrinter(indent=2)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
IN_DATA_PATH = DIR_PATH + '\\data\\interim-report-Q42020.txt'
OUT_DATA_PATH = DIR_PATH + '\data\interim-report-Q42020-filtered.txt'

def contains_amount(sent):
  regex = re.compile(r'–?[\d+,\d+|\d]+m')
  return re.search(regex, sent)

def extract_amount(sent):
  regex = re.compile(r'(–?[\d+,\d+|\d]+m)')
  return re.search(regex, sent).group(1)

sents_with_amounts = []
amounts = []
with open(IN_DATA_PATH, 'r', encoding='utf8') as f:
  lines = f.readlines()
  for sent in lines:
    if contains_amount(sent):
      sents_with_amounts.append(sent)
      amount = extract_amount(sent)
      amounts.append(amount)

with open(OUT_DATA_PATH, 'w', encoding='utf8') as f:
  for sent in sents_with_amounts:
    f.write(sent)

