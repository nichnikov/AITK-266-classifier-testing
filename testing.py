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
for text in test_texts[:100]:
    search_dict = {"pubid": 9,
                   "text": text}
    fa_r = requests.post(fa_url, json=search_dict)
    cl_r = requests.post(cl_url, json=search_dict)
    jaccard_search.append(fa_r.json())
    classifier_search.append(cl_r.json())
print("working time:", time.time() - t)

classifier_search_df = pd.DataFrame(classifier_search)
jaccard_search_df = pd.DataFrame(jaccard_search)

print(classifier_search_df)

classifier_search_df.to_csv(os.path.join("results", "classifier.csv"), sep="\t")
jaccard_search_df.to_csv(os.path.join("results", "jaccard.csv"), sep="\t")

print(classifier_search[:10])
print(jaccard_search[:10])
print(len(classifier_search), len(jaccard_search))