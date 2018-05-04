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
        temp_genre=""
        if json.loads(dd)['genres']:
            for j in range(len(json.loads(dd)['genres'])):
                temp_genre = temp_genre + json.loads(dd)['genres'][j]['name'].replace("& ", "") + " "
            g = temp_genre[:-1]
        else:
            g = ""
        if json.loads(dd)['episode_run_time']:
            r= float(json.loads(dd)['episode_run_time'][0])/100.0
        else:
            r= 0.4
        return g,r
    else:
        return "",0.4
    

def data_col(filepath):
    genres={}
    runtime={}
    df = pd.read_csv(filepath)
    pages = list(set(df["page"]))
    for i in range(len(pages)):
        txt = ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', pages[i])).lower().replace(" ","%20")
        try:
            genres[pages[i]],runtime[pages[i]]=get_gr(txt)
        except:
            #print(i)
            time.sleep(3) 
            genres[pages[i]],runtime[pages[i]]=get_gr(txt)

    gen=[]
    rt=[]
    for i in range(len(df["page"])):
        gen.append(genres[df["page"][i]])
        rt.append(runtime[df["page"][i]])
    return gen,rt
        


gen,rt = data_col("../data/spoilers/train.csv")
gen_test,rt_test = data_col("../data/spoilers/test.csv")




with open("gen.txt", "wb") as fp:
    pickle.dump(gen, fp)
with open("rt.txt", "wb") as fp:
    pickle.dump(rt, fp)
with open("gen_test.txt", "wb") as fp:
    pickle.dump(gen_test, fp)
with open("rt_test.txt", "wb") as fp:
    pickle.dump(rt_test, fp)
    
with open("gen.txt", "rb") as fp:
    gen = pickle.load(fp)
with open("rt.txt", "rb") as fp:
    rt = pickle.load(fp)
with open("gen_test.txt", "rb") as fp:
    gen_test = pickle.load(fp)
with open("rt_test.txt", "rb") as fp:
    rt_test =  pickle.load(fp)
