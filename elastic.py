from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import time 

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

def init_dict():
    # making dictionray
    src_ips = {}
    src_ips['192.168.56.12'] = {}
    src_ips['192.168.56.12']['cnt'] = 0
    src_ips['192.168.56.12']['len'] = []
    src_ips['192.168.56.12']['ttl'] = []
    src_ips['192.168.56.12']['dport'] = []

    src_ips['another_ip'] = {}
    src_ips['another_ip']['cnt'] = 0
    src_ips['another_ip']['ttl'] = []
    src_ips['another_ip']['len'] = []
    src_ips['another_ip']['dport'] = []   
    return src_ips

# process data
def get_data(s):
    total = s.count()
    print("all hits : {}".format(total))
    s.execute()
    src_ips = init_dict()

    for idx, hit in enumerate(s.scan()):
        # counting packets
        if hit.src_ip == '192.168.56.12':
            src_ips[hit.src_ip]['cnt'] += 1
            src_ips[hit.src_ip]['ttl'].append(hit.ttl)
            src_ips[hit.src_ip]['len'].append(hit.len)
            src_ips[hit.src_ip]['dport'].append(hit.dpt)
        else:
            src_ips['another_ip']['cnt'] += 1
            src_ips['another_ip']['ttl'].append(hit.ttl)
            src_ips['another_ip']['len'].append(hit.len)
            src_ips['another_ip']['dport'].append(hit.dpt)
    print(src_ips.keys())
    return src_ips
    
def draw_line(keys, ax):
    ax.scatter(c='tab:orange', label="normal")
    ax.scatter(c='tab:green', label="dos")

def draw_bar(keys, ax, cnts):
    ax.bar(list(keys.keys()), cnts, align='center', alpha=0.5)
       
def draw_scatter(keys, ax, x_axis, y_axis):
    ax.scatter(
            keys['192.168.56.12'][x_axis], 
            keys['192.168.56.12'][y_axis], 
            c='tab:green', label="dos")
    ax.scatter(
            keys['another_ip'][x_axis], 
            keys['another_ip'][y_axis], 
            c='tab:orange', label="normal")
 
# def filter_keys(src_ips):
#     keys = {}
#     cnts = []
#     for key in list(src_ips.keys()):
#         if src_ips[key]['cnt'] > 1:
#             keys[key] = {}
#             cnts.append(src_ips[key]['cnt'])
#             keys[key]['ttl'] = src_ips[key]['ttl']
#             keys[key]['len'] = src_ips[key]['len']
#             keys[key]['dport'] = src_ips[key]['dport']
#     return keys, cnts
   

# update pyplot window
def update(s):
    keys = get_data(s)
    #keys, cnts = filter_keys(src_ips)
    #draw_line(keys, ax1)
    #draw_bar(keys, ax2, cnts)
    #draw_bar(keys, ax3, cnts)
    print(keys)
    draw_scatter(keys, ax4, x_axis='dport', y_axis='ttl')
    draw_scatter(keys, ax5, x_axis='len', y_axis='dport')
    draw_scatter(keys, ax6, x_axis='len', y_axis='ttl')

#animation = FuncAnimation(fig, lambda x: update(s), interval=100)
update(s)
plt.show()
