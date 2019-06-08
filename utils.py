from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import time 
from itertools import groupby
from utils import *
import datetime

def init_dict():
    # making dictionary
    src_ips = {}
    src_ips['192.168.56.12'] = {}
    src_ips['192.168.56.12']['cnt'] = 0
    src_ips['192.168.56.12']['len'] = []
    src_ips['192.168.56.12']['ttl'] = []
    src_ips['192.168.56.12']['dport'] = []
    src_ips['192.168.56.12']['time'] = []

    src_ips['another_ip'] = {}
    src_ips['another_ip']['cnt'] = 0
    src_ips['another_ip']['len'] = []
    src_ips['another_ip']['ttl'] = []
    src_ips['another_ip']['dport'] = []
    src_ips['another_ip']['time'] = []
    return src_ips

def get_data(s):
    total = s.count()
    print("all hits: {}".format(total))
    s.execute()
    src_ips = init_dict()

    for idx, hit in enumerate(s.scan()):
        if hit.src_ip == '192.168.56.12':
            src_ips[hit.src_ip]['cnt'] += 1
            src_ips[hit.src_ip]['ttl'].append(hit.ttl)
            src_ips[hit.src_ip]['len'].append(hit.len)
            src_ips[hit.src_ip]['dport'].append(hit.dpt)
            src_ips[hit.src_ip]['time'].append(hit['@timestamp'])
        else:
            src_ips['another_ip']['cnt'] += 1
            src_ips['another_ip']['ttl'].append(hit.ttl)
            src_ips['another_ip']['len'].append(hit.len)
            src_ips['another_ip']['dport'].append(hit.dpt)
            src_ips['another_ip']['time'].append(hit['@timestamp'])
    return src_ips

def get_time_set(time_list):
    time_set = set(time_list)
    dates = list(map(lambda x: datetime.datetime.strptime(x.split('.')[0], "%Y-%m-%dT%H:%M:%S"), list(time_set)))
    traffic = [time_list.count(x) for x in time_set]
    return dates, traffic

def draw_line(keys, ax):
    normal_time_list, normal_traffic = get_time_set(
            keys['another_ip']['time'])
    dos_time_list, dos_traffic = get_time_set(
            keys['192.168.56.12']['time'])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.plot(normal_time_list, normal_traffic, c='tab:orange', label="normal")
    ax.plot(dos_time_list, dos_traffic, c='tab:green', label="dos")

def draw_bar(keys, ax, cnts):
    ax.bar(list(keys.keys()), cnts, align='center', alpha=0.5)

def draw_scatter(keys, ax, x_axis, y_axis):
    ax.scatter(
            keys['192.168.56.12'][x_axis],
            keys['192.168.56.12'][y_axis],
            c='tab:green', label='dos')
    ax.scatter(
            keys['another_ip'][x_axis],
            keys['another_ip'][y_axis],
            c='tab:orange', label='normal')

def update(s, ax1, ax2, ax3, ax4, ax5, ax6):
    keys = get_data(s)
    draw_line(keys, ax1)
    draw_scatter(keys, ax4, x_axis='dport', y_axis='ttl')
    draw_scatter(keys, ax5, x_axis='len', y_axis='dport')
    draw_scatter(keys, ax6, x_axis='len', y_axis='ttl')
        


          



