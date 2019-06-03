from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()

s = Search(using=client, index="logstash*") \
        .query("match", src_ip="172.217.25.106")

response = s.execute()

for hit in response:
    print(hit.src_ip)
