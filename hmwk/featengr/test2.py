# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 12:54:38 2018

@author: prana
"""
import pandas as pd
from nltk import word_tokenize
from nltk.tag import StanfordNERTagger,StanfordPOSTagger
import pickle

model = 'stanford-ner-2017-06-09/classifiers/english.all.3class.distsim.crf.ser.gz'
jar = 'stanford-ner-2017-06-09/stanford-ner.jar'
ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')

jar2 = 'stanford-postagger-2017-06-09/stanford-postagger.jar'
model2 = 'stanford-postagger-2017-06-09/models/english-bidirectional-distsim.tagger'
pos_tagger = StanfordPOSTagger(model2, jar2, encoding='utf8')

pos=[]
nerts=[]

df = pd.read_csv("../data/spoilers/train.csv")

for i in range(len(df['sentence'])):
    nerts.append(' '.join([ y for (x,y) in ner_tagger.tag(word_tokenize(df['sentence'][i])) if y!='O']))
    pos.append(' '.join([ y for (x,y) in pos_tagger.tag(word_tokenize(df['sentence'][i])) if y in ['VB','VBD','VBG','VBN','VBP','VBZ']]))


df = pd.read_csv("../data/spoilers/test.csv")

nerts_test=[]
pos_test=[]

for i in range(len(df['sentence'])):
    nerts_test.append(' '.join([ y for (x,y) in ner_tagger.tag(word_tokenize(df['sentence'][i])) if y!='O']))
    pos_test.append(' '.join([ y for (x,y) in pos_tagger.tag(word_tokenize(df['sentence'][i])) if y in ['VB','VBD','VBG','VBN','VBP','VBZ']]))

with open("nerts_test.txt", "wb") as fp:
    pickle.dump(nerts_test, fp)
    
with open("pos_test.txt", "wb") as fp:
    pickle.dump(pos_test, fp)
    
    
senty = np.array([0,0,0,0,0,0])
        for idx,sentence in enumerate(dfTrain["sentence"]):
            ss = sid.polarity_scores(sentence)
            temp = np.array([ss['compound'],ss['neg'], ss['neu'], ss['pos'], float(sum(1 for c in sentence if c.isupper()))/float(len(sentence)),float(rt[idx])])
            senty = np.vstack((senty,temp))
        senty = senty[1:]
        
axx = coo_matrix(self.X_train)
        self.allsentytrain = sparse.csr_matrix(hstack([axx,senty]))
        
axxval =coo_matrix(self.X_val)
            self.allsentyval = sparse.csr_matrix(hstack([axxval,senty[-500:]]))
            
senty = np.array([0,0,0,0,0,0])
        for idx,sentence in enumerate(dfTest["sentence"]):
            ss = sid.polarity_scores(sentence)
            temp = np.array([ss['compound'],ss['neg'], ss['neu'], ss['pos'], float(sum(1 for c in sentence if c.isupper()))/float(len(sentence)),float(rt_test[idx])])
            senty = np.vstack((senty,temp))
        senty = senty[1:]
        
axx = coo_matrix(self.X_test)
        self.allsentytest = sparse.csr_matrix(hstack([axx,senty]))
        
        
temp=0
c=0
for i in range(len(ep)):
    if ep[i]!=0.0:
        temp = temp + ep[i]
        c=c+1
avg = temp/c

for i in range(len(ep_test)):
    if ep_test[i]==0.0:
        ep_test[i] = 1.3