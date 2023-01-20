import os
import aiohttp
import asyncio
import pandas as pd
import time


async def searching(session, url, data):
    async with session.post(url, json=data) as resp:
        return await resp.json()


async def search(send_data: {}, urls_for_searching: []):
    results = []
    conn = aiohttp.TCPConnector(limit=10)
    timeout_seconds = 1
    session_timeout = aiohttp.ClientTimeout(sock_connect=timeout_seconds, sock_read=timeout_seconds)
    async with aiohttp.ClientSession(connector=conn, timeout=session_timeout) as session:
        tasks = []
        for url in urls_for_searching:
            tasks.append(asyncio.ensure_future(searching(session, url, send_data)))
        taking_responses = await asyncio.gather(*tasks)
    for response in taking_responses:
        results.append(response)
    return results


fa_url = "http://srv01.nlp.dev.msk2.sl.amedia.tech:4021/api/search"
cl_url = "http://srv01.nlp.dev.msk2.sl.amedia.tech:4022/api/search"

df = pd.read_csv(os.path.join("data", "queries.csv"), sep="\t")
df["text"] = df["text"].str.replace(r"\s+", " ")
test_texts = list(df["text"])

classifier_search = []
jaccard_search = []

search_data = [{"pubid": 9, "text": tx} for tx in test_texts[:100]]
results = []
t = time.time()
for search_dict in search_data:
    loop = asyncio.new_event_loop()
    res = loop.run_until_complete(search(search_dict, [fa_url, cl_url]))
    results.append(tuple(res))
print(time.time() - t)

print(results[:10])
print(len(results))
