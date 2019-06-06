from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import matplotlib.pyplot as plt
import numpy as np

client = Elasticsearch()

s = Search(using=client, index="logstash*") \
        .exclude("multi_match", query="_grokparsefailure 8.8.8.8", fields=['tags', 'src_ip']) \
        .filter("range", **{"len":{"from":0}}) \
        .filter("range", **{"ttl":{"from":0}})

total = s.count()
print("all hits : {}".format(total))
response = s.execute()

src_ips = {}

# making dictionray
for idx, hit in enumerate(s.scan()):
    # counting packets
    if hit.src_ip in src_ips:
        src_ips[hit.src_ip]['cnt'] += 1
        src_ips[hit.src_ip]['ttl'].append(hit.ttl)
        src_ips[hit.src_ip]['len'].append(hit.len)
    else:
        src_ips[hit.src_ip] = {}
        src_ips[hit.src_ip]['cnt'] = 1
        src_ips[hit.src_ip]['ttl'] = []
        src_ips[hit.src_ip]['len'] = []

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

keys = {}
cnts = []
for key in list(src_ips.keys()):
    if src_ips[key]['cnt'] > 100:
        keys[key] = {}
        cnts.append(src_ips[key]['cnt'])
        keys[key]['ttl'] = src_ips[key]['ttl']
        keys[key]['len'] = src_ips[key]['len']

keys['192.168.56.12']['ttl'] = np.array(keys['192.168.56.12']['ttl'])
ttl_indexes = np.argsort(keys['192.168.56.12']['ttl'])
ax1.scatter(keys['192.168.56.12']['ttl'][ttl_indexes], keys['192.168.56.12']['len'], c='tab:green', label="dos")
ax1.scatter(keys['111.111.111.222']['ttl'], keys['111.111.111.222']['len'], c='tab:orange', label="normal")

ax2.bar(list(keys.keys()), cnts, align='center', alpha=0.5)
plt.show()
