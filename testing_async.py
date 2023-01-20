import os
import aiohttp
import asyncio
import requests
import pandas as pd


async def searching(session, url, data):
    async with session.post(url, json=data) as resp:
        response = await resp.json()
        return response


async def search(send_data: {}, urls_for_searching: []):
    results = []
    conn = aiohttp.TCPConnector(limit=10)
    timeout_seconds = 1
    session_timeout = aiohttp.ClientTimeout(sock_connect=timeout_seconds, sock_read=timeout_seconds)
    async with aiohttp.ClientSession(connector=conn, timeout=session_timeout) as session:
        tasks = []
        for url, sign in urls_for_searching:
            tasks.append(asyncio.ensure_future(searching(session, url, send_data)))
        try:
            taking_responses = await asyncio.gather(*tasks)
        except:
            return {"templateId": 0, "templateText": ""}
    for response in taking_responses:
        results.append(response)


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


    '''
    fa_r = requests.post(fa_url, json=search_dict)
    cl_r = requests.post(cl_url, json=search_dict)
    jaccard_search.append(fa_r)
    classifier_search.append(cl_r)'''
