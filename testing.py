import os
import requests
import time
import pandas as pd

fa_url = "http://srv01.nlp.dev.msk2.sl.amedia.tech:4021/api/search"
cl_url = "http://srv01.nlp.dev.msk2.sl.amedia.tech:4022/api/search"

df = pd.read_csv(os.path.join("data", "queries.csv"), sep="\t")
df["text"] = df["text"].str.replace(r"\s+", " ")
test_texts = list(df["text"])

classifier_search = []
jaccard_search = []

t = time.time()
for k, text in enumerate(test_texts):
    search_dict = {"pubid": 9,
                   "text": text}
    fa_r = requests.post(fa_url, json=search_dict)
    cl_r = requests.post(cl_url, json=search_dict)
    fa_r_dct = fa_r.json()
    cl_r_dct = cl_r.json()
    fa_r_dct["query"] = text
    cl_r_dct["query"] = text
    jaccard_search.append(fa_r_dct)
    classifier_search.append(cl_r_dct)
    print(k, "/", len(test_texts))

classifier_search_df = pd.DataFrame(classifier_search)
jaccard_search_df = pd.DataFrame(jaccard_search)
classifier_search_df.to_csv(os.path.join("results", "classifier.csv"), sep="\t", index=False)
jaccard_search_df.to_csv(os.path.join("results", "jaccard.csv"), sep="\t", index=False)

