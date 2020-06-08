from pytrends.request import TrendReq
import spacy

pytrends = TrendReq()
z = pytrends.trending_searches(pn='united_kingdom')
nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a sentence.")
for token in doc:
    print(token.text, token.lemma_, token.pos_)

print("hello")
