'''
Created on Dec 21, 2015

@author: ben
'''
import requests

import json

import threading

import time

import random
#import csv
from Parser import MyClass

class Campaign(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, threadID):
        
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.status="started"
        print("start thread"+str(threadID))

    def getPage(self, getarg ):
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

 
    def get_data_set(self,i): 
        dataset={}
        dataset['main']={}
        dataset['updates']={}
        dataset['backers']={}
        cnt=0
        while(cnt<100):
            try:
                dataset['main'] = self.getPage(i)[0]
                
                    
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
                break
            except(AttributeError,KeyError):
                r=random.random()*500
                print(str(self.threadID)+": campaign.sleep "+str(r))
                time.sleep(random.random()*500)
            cnt=cnt+1
            if(cnt==100):
                self.status="Failed on Time-out"
        return dataset

    def run(self):
        try:
            self.ds=self.get_data_set(self.threadID)
        except requests.exceptions.ConnectionError:
            self.status="ConnectionError"
        if(self.status=="started"):
            if(self.ds==[]):
                self.status="empty"
            else:
                self.status="success"
        print("finnished thread "+str(self.threadID)+ ": "+self.status)   

    
        