'''
Created on Oct 28, 2015

@author: BlackKitten
'''

from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse
from bs4 import BeautifulSoup
import re



class WebHandler(HTMLParser):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
       

    def getWebPageString(self,url):
        response = urlopen(url)
        str_html_raw=response.read()
       
        
        '''print(str_html_raw)'''
        
        str_html=str_html_raw.decode("utf-8")
        '''print(str_html)'''
        
        return str_html_raw
      
    
class Crawler(object):
    global wHandler
    
    def __init__(self):
        '''
        Constructor
        '''  
    def crawl(self,rootUrl):
        categories=[]
        countries=[]
        wHandler=WebHandler()
        rootString=wHandler.getWebPageString(rootUrl)
        '''str_pattern="/explore/"'''
        
        '''print(rootString)'''
       
        soup = BeautifulSoup(rootString)
        
        pattern=re.compile('/explore/(.*)')
        for projecta in soup.find_all(name='a'):
            '''print(project)'''
            href=projecta.get('href')
            
            try:
               
                if(pattern.match(href)):
                    print(pattern.group(1))
                    categories.append(pattern.group(1))
                    
            except TypeError:
                print("TypeError: ",href)
            except AttributeError:
                print("AttributeError: ",href)
        
        for project_country in soup.find_all(name='div'):
            try:
                if( (project_country['class'][0]=="ng-binding") & (project_country['class'][1]=="ng-scope") ):
            
                    print(project_country['value'])
            except KeyError:
                print("KeyError: ",project_country)
            except IndexError:
                print("IndexError: ",project_country)
            '''print(project_country)'''
            
            
c=Crawler()
c.crawl("https://www.fundable.com/browse")    
        
        