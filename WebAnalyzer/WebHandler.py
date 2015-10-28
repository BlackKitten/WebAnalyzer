'''
Created on Oct 28, 2015

@author: BlackKitten
'''

from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
       

    def getWebPage(self,url):
        response = urlopen(url)
        
        if response.getheader('Content-Type')=='text/html': 
           htmlString = response.read.decode("utf-8")
           return htmlString
    