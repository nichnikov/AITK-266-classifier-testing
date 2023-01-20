import os
import requests
import pandas as pd

fa_url = "http://srv01.nlp.dev.msk2.sl.amedia.tech:4021/api/search"
cl_url = "http://srv01.nlp.dev.msk2.sl.amedia.tech:4022/api/search"

df = pd.read_csv(os.path.join("data", "queries.csv"), sep="\t")
df["text"] = df["text"].str.replace(r"\s+", " ")
test_texts = list(df["text"])

classifier_search = []
jaccard_search = []

for text in test_texts[:10]:
    search_dict = {"pubid": 9,
                   "text": text}
    fa_r = requests.post(fa_url, json=search_dict)
    cl_r = requests.post(cl_url, json=search_dict)
    jaccard_search.append(fa_r)
    classifier_search.append(cl_r)
