def getdescimg(url):
	global dic,disp
	data=urllib2.urlopen(url).read()
	soup4=bs(data)
	try:
		p=soup4.find("p")
		temp=p.text
		temp=re.sub(r'\[.*\]',"",temp)
		dic["Description"]=" "+temp+" "
		disp.append("Description")
	except:
		pass
	try:
		table=soup4.find("table",class_="infobox vcard")
		soup5=bs(str(table))
		img=soup5.find("img")
		dic["Image"]=" "+img.get("src")[2:]+" "
		disp.append("Image")
	except:
		pass
import urllib2
import re
from bs4 import BeautifulSoup as bs
import pymongo
client=pymongo.MongoClient()
db=client.brainse
explorers=db.explorers
url="https://en.wikipedia.org/wiki/List_of_explorers"
d=urllib2.urlopen(url).read()
key=[]
dic={}
disp=[]
d=d.split('<table class="wikitable sortable" style="text-align:center;">')
for i in range(2,len(d)):	#len(d)
	soup=bs(str(d[i]))
	tr=soup.findAll("tr")
	soup1=bs(str(tr[0]))
	th=soup1.findAll("th")
	for j in th:
		t1=filter(lambda x:ord(x)>31 and ord(x)<128,j.text)
		if t1=="Main area/s explored":
			t1="Areas Explored"
		key.append(t1)
		disp.append(t1)
	print key
	tr=tr[1:]
	for k in range(0,len(tr)):
		soup2=bs(str(tr[k]))
		td=soup2.findAll("td")
		m=0
		disp=list(key)
		for l in td:
			temp=l.text
			if len(temp)>0:
				if key[m]=="Name":
					soup3=bs(str(l))
					a=soup3.find("a")
					e="https://en.wikipedia.org"+a.get("href")
					dic["Link"]=" "+e+" "
					getdescimg(e)
					disp.append("Link")
				dic[key[m]]=" "+temp+" "
			m=m+1
		dic["display_order"]=disp
		print dic
		explorers.insert(dic)
		dic={}
	key=[]
			
			
