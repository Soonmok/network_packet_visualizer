import seaborn as sns
import pandas as pd
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

result_df = pd.DataFrame((d.to_dict() for d in s.scan()))
result_df = result_df.drop(['@timestamp', '@version', 'geoip', 'host', 'id', 'message', 'path', 'prec', 'res', 'tags', 'tos', 'urgp', 'src_ip', 'dst_ip'], axis=1)

print(result_df)

sns.set(style="ticks", color_codes=True)
g = sns.pairplot(result_df, hue="proto")
plt.show()
