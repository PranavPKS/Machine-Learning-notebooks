# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 18:45:18 2018

@author: prana
"""

import json
import http.client
import time
import pickle
import re
import pandas as pd

def get_gr(txt):
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    conn.request("GET", "/3/search/tv?page=1&query="+txt+"&language=en-US&api_key=ffdfecf0830968b442b85db5a9cb58a9")
    data = conn.getresponse().read()
    if json.loads(data)['results']:
        id_temp = json.loads(data)['results'][0]['id']
        try:
            conn.request("GET", "/3/tv/"+str(id_temp)+"?language=en-US&api_key=ffdfecf0830968b442b85db5a9cb58a9")
        except:
            conn.request("GET", "/3/tv/"+str(id_temp)+"?language=en-US&api_key=ffdfecf0830968b442b85db5a9cb58a9")
        dd = conn.getresponse().read()
        if json.loads(dd)['first_air_date']:
            ep= float(json.loads(dd)['first_air_date'].split('-')[0])
        else:
            ep= 0.0
        return ep
    else:
        return 0.0
    

def data_col(filepath):
    episodes={}
    df = pd.read_csv(filepath)
    pages = list(set(df["page"]))
    for i in range(len(pages)):
        txt = ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', pages[i])).lower().replace(" ","%20")
        try:
            episodes[pages[i]]=get_gr(txt)
        except:
            print(i)
            time.sleep(3) 
            episodes[pages[i]]=get_gr(txt)

    ep=[]
    for i in range(len(df["page"])):
        ep.append(episodes[df["page"][i]])
    return ep
        


air = data_col("../data/spoilers/train.csv")
air_test = data_col("../data/spoilers/test.csv")

temp=0
c=0
for i in range(len(air)):
    if air[i]!=0.0:
        temp = temp + air[i]
        c=c+1
avg = temp/c

for i in range(len(air_test)):
    if air_test[i]==0.0:
        air_test[i] = 2000.0