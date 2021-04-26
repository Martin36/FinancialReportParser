import camelot
import os
import tabula

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PDF_PATH = DIR_PATH + '\\pdfs\\Interim-Report-Q42020.pdf'

def use_camelot():
  tables = camelot.read_pdf(PDF_PATH, flavor="stream", suppress_stdout=True, pages="all")

  print(tables[0].df)

  for i in range(5):
    tables[i].to_csv(DIR_PATH + '\\hoist-q42020-tables\\table-camelot-{0}.csv'.format(i+1))

def use_tabula():
  tables = tabula.read_pdf(PDF_PATH, stream=True, pages="all")

  for i in range(len(tables)):
    tables[i].to_csv(DIR_PATH + '\\hoist-q42020-tables\\table-tabula-{0}.csv'.format(i+1))


use_tabula()