from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()

s = Search(using=client, index="logstash*") \
        .exclude("multi_match", query="_grokparsefailure 8.8.8.8", fields=['tags', 'src_ip']) \
        .filter("range", **{"len":{"from":0}})

total = s.count()
print("all hits : {}".format(total))
response = s.execute()

for hit in s.scan():
    print(hit.len)
