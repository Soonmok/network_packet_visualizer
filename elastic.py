from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import time 
from utils import *

# create Elasticsearch client
client = Elasticsearch()

# search hits
s = Search(using=client, index="logstash*") \
        .filter("exists", field="src_ip") \
        .filter("exists", field="ttl") \
        .filter("exists", field="len") \
        .filter("range", **{"@timestamp":{'gte': 'now-29m', 'lt': 'now'}})
        #.exclude("multi_match", query="8.8.8.8 192.168.56.12", fields=['src_ip', 'dst_ip']) \

# configure pyplot windows
fig = plt.figure()
ax1 = fig.add_subplot(2, 3, 1)
ax2 = fig.add_subplot(2, 3, 2)
ax3 = fig.add_subplot(2, 3, 3)
ax4 = fig.add_subplot(2, 3, 4)
ax5 = fig.add_subplot(2, 3, 5)
ax6 = fig.add_subplot(2, 3, 6)


# update pyplot window
animation = FuncAnimation(fig, lambda x: update(s, ax1, ax2, ax3, ax4, ax5, ax6), interval=100)
# while True:
#     update(s, ax1, ax2, ax3, ax4, ax5, ax6)
#     print("...")
plt.show()
