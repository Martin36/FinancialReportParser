import os
import spacy

nlp = spacy.load("en_core_web_sm", exclude=["parser"])
nlp.enable_pipe("senter")

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
IN_DATA_PATH = DIR_PATH + '\\data\\vef-1q2021.txt'
# OUT_DATA_PATH = DIR_PATH + '\\data\\vef-1q2021-filtered.txt'

with open(IN_DATA_PATH, 'r', encoding='utf8') as f:
  text = f.read()

doc = nlp(text)
for sent in doc.sents:
  print(sent.text)
