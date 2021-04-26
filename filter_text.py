import os
import re
import pprint

pp = pprint.PrettyPrinter(indent=2)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEXT_PATH = DIR_PATH + '\\data\\interim-report-Q42020.txt'

with open(TEXT_PATH, 'r', encoding='utf8') as f:
  lines = f.readlines()
  filtered_lines = []
  for line in lines:
    if re.search(r'-?\d+,?\d*m', line):
      filtered_lines.append(line)
  pp.pprint(filtered_lines)
