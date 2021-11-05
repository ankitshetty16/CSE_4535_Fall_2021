# -*- coding: utf-8 -*-


import json
# if you are using python 3, you should 
import urllib.request
from urllib.parse import quote

# import urllib2

# declare parameters
AWS_IP = '3.134.101.124'
IRModels = ['bm25', 'vsm'] #either bm25 or vsm
train = False
if train == True:
    # query file to be used for training
    f = open('queries.txt','r')
else:
    # query file for final submission
    f = open('test-queries.txt','r')
documents = f.readlines()

for IRModel in IRModels:
    core = f'IRF21_p3_{IRModel}_1' #'IRF21_p3_vsm_1','IRF21_p3_bm25_1'
    print(core)

    for index, document in enumerate(documents):
        qid = document[ 0 : 4 ]
        text = document[ 4 : -1 ]

        textValue = quote(text)
        inurl = f'http://{AWS_IP}:8983/solr/{core}/select?q=text_en:{textValue}%20OR%20text_de:{textValue}%20OR%20text_ru:{textValue}&fl=id%2Cscore&wt=json&indent=true&rows=20'
        # inurl = f'http://{AWS_IP}:8983/solr/{core}/select?q=text_en:{textValue}%20OR%20text_de:{textValue}%20OR%20text_ru:{textValue}&fl=id%2Cscore&wt=json&indent=true&rows=872'
        print('>>>>>>>>>>>>>>>>>>>>>>>.')
        print(inurl)

        if train == True:
            outfn = f'trec_input_{IRModel}.txt'
        else:
            outfn = f'{IRModel}/{index+1}.txt'

        print('MY OUTPUT FILE PATH>> ',outfn)       
        outf = open(outfn, 'a+')

        data = urllib.request.urlopen(inurl)

        docs = json.load(data)['response']['docs']
        # the ranking should start from 1 and increase
        rank = 1
        for doc in docs:
            outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
            rank += 1
        outf.close()
