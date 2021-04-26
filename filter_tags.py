import os, re, csv, pprint
import pandas as pd

pp = pprint.PrettyPrinter(indent=2)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = DIR_PATH + '\\data\\num.tsv'

adsh = "0001640334-20-002446"
data = pd.read_csv(DATA_PATH, sep='\t')
print(data.shape)

adsh_filter = data['adsh'] == adsh
filtered_data = data[adsh_filter]
print(filtered_data.shape)
print(filtered_data)

filtered_data.to_csv(DIR_PATH + '\\data\\filtered_num.tsv', sep='\t')


# with open(DATA_PATH, 'r', encoding='utf8') as fd:
#   rd = csv.reader(fd, delimiter"\t", quotechar='"')
#   headers = 

