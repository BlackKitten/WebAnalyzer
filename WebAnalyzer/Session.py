#!/usr/bin/python
'''
Created on Nov 28, 2015

@author: ben



'''

import requests

import json

import csv

from Parser import MyClass

labels=[]

def getPage( getarg ):
    r = requests.get('http://www.idea.me/projects')
    headers = {'Host':'www.idea.me', 
        'Connection':'keep-alive', 
        'Accept':'application/json, text/javascript, */*; q=0.01', 
        'X-Requested-With':'XMLHttpRequest', 
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36 DNT: 1', 
        'Referer':'http://www.idea.me/projects', 
        'Accept-Encoding':'gzip, deflate, sdch', 
        'Accept-Language':'en-US,en;q=0.8,nl;q=0.6,fr;q=0.4', 
        'Cookie':''}
    headers['Cookie'] = r.headers['Set-Cookie']
    r = requests.get('http://www.idea.me/projects', headers=headers, params='from='+str(getarg))
    json_data = r.json()
    return json_data

def putLabels(dataset):
    labels=[]
    for row in dataset :
        #print("row:"+ str(row))
        for column in row.items():
            try:
                #print("column: "+str(column))
                int_length=len(column)
                if(int_length>1):
                    try:
                        for sublabel in column.items():
                            temp_name=column[0]+"."+sublabel[0]
                            if not(temp_name in labels):
                                labels.append(temp_name)
                    except AttributeError:
                        if not(column[0] in labels):
                            labels.append(column[0])
                if not(column[0] in labels):
                    labels.append(column[0])
            except TypeError:
                if not(column[0] in labels):
                    labels.append(column[0])
   
    
    #f1 = open('test_out.csv','w')
   
    
#    for label in labels:
#          
#        try:
#            int_length=len(label_data[0][d])
#            if (int_length>1) :
#                try:
#                    for dd in label_data[0][d].items():
#                        labels.append(d+"."+dd[0])
#                except AttributeError:
#                    labels.append(d)
#            else:
#                labels.append(d)
#                
#        except TypeError:
#            labels.append(d)
    print(labels)        
    #writer = csv.DictWriter(f1,fieldnames=labels,delimiter="§")
    #writer.writeheader() 
    #f1.close()
    return labels
 
def get_data_set(i): 
    dataset={}
    dataset['main']={}
    dataset['updates']={}
    dataset['backers']={}
    dataset['main'] = getPage(i)[0]
    parser=MyClass()
    parser.parse_project_page("http://www.idea.me"+dataset['main']['url'])
    parser.parse_campaigner_bio("http://www.idea.me"+dataset['main']['url'])
    parser.parse_backers(dataset['main']['id'])   
    parser.parse_updates(dataset['main']['id'])
    dataset['main'].update(parser.stuff)  
    dataset['main']['fb_likes']=parser.get_fb_likes(dataset['main']['url'])
    
    dataset['backers']=parser.backers
    dataset['backers']['projectnr']=dataset['main']['id']
    
    dataset['updates']=parser.updates
    dataset['updates']['projectnr']=dataset['main']['id']
    #print("json_data")
    #print(json_data)
    return dataset
def printToFile(dataset,labels,fn):
    #json_data = getPage(i)
    #parser=MyClass()
    #parser.parse_project_page(json_data['url'])
    #parser.parse_campaigner_bio(json_data['url'])
    #parser.parse_backers(json_data['id'])
    
    #json_data.update(parser.stuff)
    
    json_data=dataset
    length=str(len(json_data))
    print("dataset length: "+length)
    if(length==0):
        raise Exception
    f1 = open(fn,'a')
    writer = csv.DictWriter(f1,fieldnames=labels,delimiter="§")
    writer.writeheader()
        
    campaigns=[]
    
    for d in json_data:
        '''print(d)'''
        campaign={}
        for title in labels:
            
                
            try:
                if("." in title):
                    lbl1=title.split(".")[0]
                    lbl2=title.split(".")[1]
                    campaign[title]=d[lbl1][lbl2]
                else:
                    if("summary" in title):
                        campaign[title]=len(d[title])
                    else:    
                        campaign[title]=d[title]
            except KeyError:
                print("KeyError: " +title)
        campaigns.append(campaign)
    
    for campaign in campaigns:
        writer.writerow(campaign)
         
    f1.close()


i=1
dataset={}
dataset['main']=[]
dataset['updates']=[]
dataset['backers']=[]

try:
    while(True):
        try:
            ds=get_data_set(i)
        except requests.exceptions.ConnectionError:
            print("ConnectionError @ "+i)
            i=i+1
            ds=get_data_set(i)
        dataset['main'].append(ds['main'])
        dataset['updates'].append(ds['updates'])
        dataset['backers'].append(ds['backers'])
        
    
        i=i+1
        print(i)
except Exception:
    print("Exception")
    
print("writing dataset")
labels=putLabels(dataset['main'])
printToFile(dataset['main'],labels,"gb_main.csv")
labels=putLabels(dataset['backers'])
printToFile(dataset['backers'],labels,"gb_backers.csv")
labels=putLabels(dataset['updates'])
printToFile(dataset['updates'],labels,"gb_updates.csv")
print("Finished")
    
    
    