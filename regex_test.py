import re

# def repl(m):
# reg = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s")
reg = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z]\.)(?<=\.|\?)\s")
input_text = "Cash flow from financing activities totalled 396m (–1,963). Net cash flow from deposits from the public totalled SEK –563m (–224) during the quarter. The bond issue and repurchase conducted during the quarter resulted in a cash flow of SEK 988m. The quarter’s repayment of bonds in securitisation company Marathon SPV S.r.l. totalled SEK –17m (–). Other cash flow from financing activities totalled SEK –12m (–11) and pertains to amortisation of lease liability."
sentences = re.split(reg, input_text)
print(sentences)
