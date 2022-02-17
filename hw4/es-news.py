from elasticsearch.client import Elasticsearch
import time
import json
with open('./nknews//news2.json','r',encoding='utf-8')as fp:
    json_data = json.load(fp)
es = Elasticsearch()

if __name__ == "__main__":
    res = es.indices.delete('newstore-index')
    for i in range(17279,17279+len(json_data)-1):
        json_data[i-17278]['content'] = str(json_data[i-17278]['content'])
        res = es.index(index="newstore-index", id=i, document=json_data[i-17278])
    time.sleep(10)
    print(i)
    print(type(json_data[i]['links']))