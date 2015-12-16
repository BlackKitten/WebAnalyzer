'''
Created on Dec 8, 2015

@author: ben
'''

import requests
import re

class MyClass(object):

	def __init__(self):
		self.stuff={}        
	def getPage(self,url ):
		r = requests.get('http://www.idea.me/projects')
		headers = {'Host':'www.idea.me', 
            'Connection':'keep-alive', 
            'Cache-Control':'max-age=0',
            'Accept':'application/json, text/javascript, */*; q=0.01', 
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36 DNT: 1', 
            'DNT':'1', 
            'Accept-Encoding':'gzip, deflate, sdch', 
            'Accept-Language':'en-US,en;q=0.8,nl;q=0.6,fr;q=0.4', 
            'Cookie':''}
		headers['Cookie'] = r.headers['Set-Cookie']
		r = requests.get(url, headers=headers)
		html_data = r.text
        #print(r.url)
		return html_data
    
	def get_json_data(self,projectnr,size,data_key):
		r = requests.get('http://www.idea.me/projects/'+str(projectnr))
        #print(r.text)
		headers = {'Host':'www.idea.me', 
            'Connection':'keep-alive', 
            #'Cache-Control':'max-age=0',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept':'application/json, text/javascript, */*; q=0.01', 
            #'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36 DNT: 1', 
            'DNT':'1', 
            'Accept-Encoding':'gzip, deflate, sdch', 
            'Accept-Language':'en-US,en;q=0.8,nl;q=0.6,fr;q=0.4', 
            'Cookie':'',
            'Refer':'http://www.idea.me/projects/'+str(projectnr)}
		headers['Cookie'] = r.headers['Set-Cookie']
		if(data_key=="backers"):
			payload = {'size':''+str(size),'from':'0'}
		if(data_key=="updates"):
			payload = {'offset':''+str(size)}
		r = requests.get('http://www.idea.me/projects/'+str(projectnr)+'/'+data_key,headers=headers,params=payload)
		print(r.url)
		return r.json()
       
        
	def processUrl(self,url):
		html_data=self.getPage(url)
        #print(html_data)
		self.parse_project_page(html_data)

	def parse_project_page(self,url):
		html_data=self.getPage(url)
        #print(html_data)
        #TODO add none catch 4 counters
		match = re.search(r'filtro categoria">\n\s+([A-Za-z]+)',html_data)
		self.stuff['category']=match.group(1)
		match = re.search(r'imágenes</a>\s*<[a-z ="]+>([0-9]+)', html_data)
		self.stuff['images']=match.group(1)
		match = re.search(r'updatesCant" class="cant">([0-9]*)', html_data)
		self.stuff['updates']=match.group(1)
		match=re.search(r'colaboradores</a>\s*<div class="cant">([0-9]*)',html_data)
		self.stuff['backers']=match.group(1)
		match=re.search(r'comentarios</a>\s*<div class="cant">([0-9]*)',html_data)
		self.stuff['comments']=match.group(1)
		match=re.search(r'Seguir"[/>\s<a-z]+([0-9]*)',html_data)
		self.stuff['followers']=match.group(1)
		matches = tuple(re.finditer('box rewardBox',html_data))
		self.stuff['#rewards']=len(matches)
		match=re.search(r'Financiado! :\)[^0-9]+([^<]*)', html_data)
		try:
			self.stuff['Date reached']=match.group(1)
		except(AttributeError):
			self.stuff['Date reached']=""
			
		match=re.search('class="videoContent"',html_data)
		try:
			self.stuff['video']= (len(match.group(0))>0) 
		except(AttributeError):
			self.stuff['video']=False

	def parse_campaigner_bio(self,url):
		html_data=self.getPage(url)
        
		match = re.search(r'class=\"clear\">(</div>\s*){2}((<p>.*</p>\s*)+)', html_data)
		try:
			self.stuff['bio']=len(match.group(2))
		except(AttributeError):
			self.stuff['bio']=0
        
	def parse_backers(self,projectnr):
		int_size=self.get_json_data(projectnr, 1,"backers")['total']
		backers=(self.get_json_data(projectnr,int_size,"backers")['backers'])
		date_counter={}
		for backer in backers:
			key=backer['creationDate'][:10].replace("-","/")
            
            
			if (key in date_counter.keys()):
				date_counter[key]= date_counter[key]+1                
			else:
				date_counter[key]=1
		self.backers=date_counter
	def parse_updates(self,projectnr):
		updates_temp=self.get_json_data(projectnr, 0,"updates")
		updates=updates_temp
		while(len(updates_temp)>0):
			updates_temp=self.get_json_data(projectnr, len(updates), "updates")
			for update_t in updates_temp:
				updates.append(update_t)
		#updates=(self.get_json_data(projectnr, int_size, "updates"))
		date_counter={}
		for update in updates:
			print(update)
			try:
				key=update['updateDate'][:10].replace("-","/")
			
				if (key in date_counter.keys()):
					date_counter[key]=date_counter[key]+1
				else:
					date_counter[key]=1
			except(TypeError):
				print(TypeError)
		self.updates=date_counter
	def get_html_data(self,url):
		return self.getPage(url)
	def get_fb_likes(self,url):
		fb_url="http://www.idea.me"+url
		fb_url=fb_url.replace(":","%3A")
		fb_url=fb_url.replace("/","%2F")
		
		r_likes=requests.get("https://www.facebook.com/plugins/like.php?action=like&app_id=1549005192016984&channel=http%3A%2F%2Fstatic.ak.facebook.com%2Fconnect%2Fxd_arbiter.php%3Fversion%3D42%23cb%3Df82b413c%26domain%3Dwww.idea.me%26origin%3Dhttp%253A%252F%252Fwww.idea.me%252Ff26572cf1%26relation%3Dparent.parent&container_width=82&href="+fb_url+"&layout=button_count&locale=en_US&sdk=joey&send=false&show_faces=false")
		match=re.search('pluginCountTextConnected">([0-9.k]+)', r_likes.text)
		return match.group(1)
		#print(html)
test=MyClass()
#test.parse_updates("30407")
#html_data1=test.get_html_data("http://www.idea.me/projects/34728/muertos-de-amor-y-de-miedo")
#html_data2=test.get_html_data("http://www.idea.me/proyectos/20903/hoysalimos")
#test.parse_project_page('http://www.idea.me/projects/34728/muertos-de-amor-y-de-miedo')
#test.parse_campaigner_bio('http://www.idea.me/projects/34728/muertos-de-amor-y-de-miedo')
#test.parse_backers('34728')

#print(test.stuff)
#print(test.backers)
#test.parse_campaigner_bio('http://www.idea.me/projects/34728/muertos-de-amor-y-de-miedo')


#test.parse_backers("http://www.idea.me/projects/34728/muertos-de-amor-y-de-miedo")
#test.parse_campaigner_bio("http://www.idea.me/projects/32337/fernando-garcia-curten---libro")
#test.parse_project_page("http://www.idea.me/projects/34728/muertos-de-amor-y-de-miedo")
