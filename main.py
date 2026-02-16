import spacy

nlp = spacy.load("en_core_web_sm")

document = '''Mark Zuckerberg laid out the future of the company in a keynote address at the company's annual developer conference.'''

doc = nlp(document)

for e in doc:
  if e.ent_type_ != "":
    print(f"{e} | {e.ent_type_}")