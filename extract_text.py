import os
import fitz
import re

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PDF_PATH = DIR_PATH + '\\pdfs\\vef-1q21.pdf'
OUT_FILE = 'vef-1q2021.txt'
NR_OF_PAGES_TO_EXTRACT = 5
START_PAGE = 1  # index start at 0

with fitz.open(PDF_PATH) as doc:
  text = ""
  for i, page in enumerate(doc):
    if i > NR_OF_PAGES_TO_EXTRACT:
      break
    if i < START_PAGE:
      continue
    page_text = page.getText()
    page_text = re.sub(r"[“”]", " ", page_text)
    text_tokens = page_text.split("\n")
    # Remove empty strings
    text_tokens = [token for token in text_tokens if len(token) > 0]
    # Remove short strings and the once that contain special char
    text_tokens = [token for token in text_tokens if len(
        token) > 20 or token[-1] == '.']
    text_tokens = [
        token for token in text_tokens if not re.search(r'•', token)]
    raw_text = "".join(text_tokens)
    # RegEx that should match end of sentences but not abbrivations
    reg = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z]\.)(?<=\.|\?)\s")
    sentences = re.split(reg, raw_text)
    sentences = [sent.strip() for sent in sentences]
    text += "\n".join(sentences)
  # print(text)
  # doc.close()

  with open("{}\\data\\{}".format(DIR_PATH, OUT_FILE), "w", encoding='utf8') as text_file:
    text_file.write(text)
    # text_file.close()
