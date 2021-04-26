import os
import fitz
import re

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PDF_PATH = DIR_PATH + '\\pdfs\\Interim-Report-Q42020.pdf'
with fitz.open(PDF_PATH) as doc:
  text = ""
  for i, page in enumerate(doc):
    if i > 5:
      break
    page_text = page.getText()
    page_text = re.sub(r"[“”]", " ", page_text)
    text_tokens = page_text.split("\n")
    # Remove empty strings
    text_tokens = [token for token in text_tokens if len(token) > 0]
    # Remove short strings and the once that contain special char
    text_tokens = [token for token in text_tokens if len(token) > 20 or token[-1] == '.']
    text_tokens = [token for token in text_tokens if not re.search(r'•', token)]
    raw_text = "".join(text_tokens)
    # RegEx that should match end of sentences but not abbrivations
    reg = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z]\.)(?<=\.|\?)\s")
    sentences = re.split(reg, raw_text)
    sentences = [sent.strip() for sent in sentences]
    text += "\n".join(sentences)
  # print(text)
  # doc.close()

  with open(DIR_PATH + "\\data\\interim-report-Q42020.txt", "w", encoding='utf8') as text_file:
    text_file.write(text)
    # text_file.close()
  
