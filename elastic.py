from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import matplotlib.pyplot as plt

client = Elasticsearch()

s = Search(using=client, index="logstash*") \
        .exclude("multi_match", query="_grokparsefailure 8.8.8.8", fields=['tags', 'src_ip']) \
        .filter("range", **{"len":{"from":0}})

total = s.count()
print("all hits : {}".format(total))
response = s.execute()

idxes = []
hits = []

for idx, hit in enumerate(s.scan()):
    idxes.append(idx)
    hits.append(hit.len)

plt.scatter(idxes, hits)
plt.yscale('log')
plt.show()
