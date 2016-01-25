'''
Created on Dec 21, 2015

@author: ben
'''
import csv
import requests
import time
from Campaign import Campaign


if __name__ == '__main__':
    print("main")

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
        return labels
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



threads = []
#try:



    
threadQ={}
for ir in range(80):
    threadQ[str(ir)]="null"
    
finished=False

campaign_number=1


while(not finished):
    found_spot=False
    for k in threadQ:
        if(threadQ[k] == "null"):
            found_spot=True
            threadQ[k]=Campaign(campaign_number)
            threadQ[k].start()
            time.sleep(0.5)
            break
        status=threadQ[k].status
        if(status=="success"):
            found_spot=True
            threads.append(threadQ[k])
            threadQ[k]=Campaign(campaign_number)
            threadQ[k].start()
            break
        if(status =="empty"):
            finished=True
            for ki in threadQ:
                threads.append(threadQ[ki])
            break
        if(status=="ConnectionError"):
            threadQ[k]=Campaign(threadQ[k].threadID)
            threadQ[k].start()
    if(found_spot):
        campaign_number=campaign_number+1
    else:
        time.sleep(0.5)
# while(i<2000):
#     d_class=Campaign(i)
#     threads.append(d_class)
#     
#     ds=d_class.start()
#     time.sleep(0.5)
#     i=i+1
#     print(i)
#  
#     if(i % 50 == 49):
#        
#         for thread in threads:
#             if(thread.status=="started"):
#                 print("sleeping on thread:"+ str(thread.threadID))
#                 wi=0
#                 while(thread.status=="started"):
#                     wi=wi+1
#                     time.sleep(1)
#                     if(wi>5):
#                         print("timeout waiting on thread "+str(thread.threadID))
#                         break
#                    
                    
# except Exception:
#     print("Exception")
   
time.sleep(60)
for thread in threads:
    i=0
    while(thread.status=="started"):
        if(i==5):
            break
        print("sleeping on "+str(thread.threadID))
        time.sleep(5)
        print("waking up")
        i=i+1
    if(thread.status=="success"):
        dataset['main'].append(thread.ds['main'])
        dataset['updates'].append(thread.ds['updates'])
        dataset['backers'].append(thread.ds['backers']) 
    if(thread.status=="empty"):
        break
    
print("writing dataset")
labels=putLabels(dataset['main'])
printToFile(dataset['main'],labels,"gb_main.csv")
labels=putLabels(dataset['backers'])
printToFile(dataset['backers'],labels,"gb_backers.csv")
labels=putLabels(dataset['updates'])
printToFile(dataset['updates'],labels,"gb_updates.csv")
print("Finished")
    