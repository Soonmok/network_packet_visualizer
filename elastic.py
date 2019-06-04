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

normal_idxes = []
normal_hits = []
dos_idxes = []
dos_hits = []

for idx, hit in enumerate(s.scan()):
    if hit.src_ip == "111.111.111.222":
        normal_idxes.append(idx)
        normal_hits.append(hit.len)
    else:
        dos_idxes.append(idx)
        dos_hits.append(hit.len)


plt.scatter(dos_idxes, dos_hits, c='tab:blue')
plt.scatter(normal_idxes, normal_hits, c='tab:orange')
plt.yscale('log')
plt.show()
