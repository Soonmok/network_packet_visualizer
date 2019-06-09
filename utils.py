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
    every_ips = {}

    for hit in s.scan():
        if hit.src_ip in every_ips:
            every_ips[hit.src_ip] += 1
        else:
            every_ips[hit.src_ip] = 0

    every_ports = {}
    for hit in s.scan():
        if hit.dpt in every_ports:
            every_ports[hit.dpt] += 1
        else:
            every_ports[hit.dpt] = 0


    for idx, hit in enumerate(s.scan()):
        if hit.src_ip == '192.168.56.12':
            src_ips[hit.src_ip]['cnt'] += 1
            src_ips[hit.src_ip]['ttl'].append(float(hit.ttl))
            src_ips[hit.src_ip]['len'].append(float(hit.len))
            src_ips[hit.src_ip]['dport'].append(float(hit.dpt))
            src_ips[hit.src_ip]['time'].append(hit['@timestamp'])
        else:
            src_ips['another_ip']['cnt'] += 1
            src_ips['another_ip']['ttl'].append(float(hit.ttl))
            src_ips['another_ip']['len'].append(float(hit.len))
            src_ips['another_ip']['dport'].append(float(hit.dpt))
            src_ips['another_ip']['time'].append(hit['@timestamp'])

    return src_ips, every_ips, every_ports

def get_time_set(time_list):
    time_list = list(map(lambda x: datetime.datetime.strptime(x.split('.')[0], "%Y-%m-%dT%H:%M:%S"), time_list))
    time_list = [str(x.date()) + str(x.time()) for x in time_list]
    time_set = sorted(set(time_list))
    traffic = [time_list.count(x) for x in time_set]
    return time_set, traffic

def draw_line(keys, ax):
    normal_time_list, normal_traffic = get_time_set(
            keys['another_ip']['time'])
    dos_time_list, dos_traffic = get_time_set(
            keys['192.168.56.12']['time'])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d-%H-%M-%S'))
    ax.plot(normal_time_list, normal_traffic, c='tab:orange', label="normal")
    ax.plot(dos_time_list, dos_traffic, c='tab:green', label="dos")
    ax.set_yticklabels([])
    ax.set_xticklabels([])

def draw_bar(every_ips, ax, limit):
    ips = []
    cnts = []
    for key in every_ips.keys():
        if every_ips[key] > limit:
            ips.append(key)
            cnts.append(every_ips[key])
    ax.bar(ips, cnts, color='tab:red', align='center')

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
    keys, every_ips, every_ports = get_data(s)
    draw_line(keys, ax1)
    ax1.set(xlabel='time', ylabel='traffic', title='Time-traffic graph')
    draw_bar(every_ips, ax2, 10)
    ax2.set(xlabel='src_ips', ylabel='counts', title='src_ips-counts bar chart')
    draw_bar(every_ports, ax3, 10)
    draw_scatter(keys, ax4, x_axis='ttl', y_axis='dport')
    ax4.set(xlabel='ttl', ylabel='dst_port', title='ttl-dst_port scatter chart')
    ax4.set_xlim([0, 100])
    draw_scatter(keys, ax5, x_axis='len', y_axis='dport')
    ax5.set(xlabel='len', ylabel='dst_port', title='len-dst_port scatter chart')
    draw_scatter(keys, ax6, x_axis='ttl', y_axis='len')
    ax6.set(xlabel='ttl', ylabel='len')
    ax6.set_xlim([0, 100])

