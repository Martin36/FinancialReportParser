import os
import pandas as pd
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PDF_PATH = DIR_PATH + '\\pdfs\\vef-1q21.pdf'


def use_pdfminer():
  pdfminer_string = StringIO()
  with open(PDF_PATH, "rb") as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr,
                           pdfminer_string,
                           laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
      interpreter.process_page(page)
  pdfminer_lines = pdfminer_string.getvalue().splitlines()
  pdfminer_lines = [ln for ln in pdfminer_lines if ln]
  print(pdfminer_lines)

  pdf_lines = pd.Series(pdfminer_lines)
  max_width = pdf_lines.str.len().max()
  pdf_lines_adjusted = pdf_lines.apply(adjust_string, args=(max_width, ))
  pdf_lines_mtx = np.stack(pdf_lines_adjusted.map(list).to_numpy())

  whitespace_сols = np.where(np.all(pdf_lines_mtx == ' ', axis=0))[0]
  rightmost_whitespace_cols = np.where(np.diff(whitespace_сols) != 1)[0]
  column_dividers = np.append(whitespace_сols[rightmost_whitespace_cols],
                              whitespace_сols[-1])

  splitted_lines = []
  for row in pdf_lines_adjusted:
    current_row = []
    for e in range(len(column_dividers) - 1):
      if e == 0:
        current_row.append(row[: column_dividers[e]].strip())
      (current_row
       .append(row[column_dividers[e]: column_dividers[e + 1]]
               .strip()))
    current_row.append(row[column_dividers[-1]:].strip())
    splitted_lines.append(current_row)


use_pdfminer()
