def getDesc(url):
	d=urllib2.urlopen(url).read()
	soup=bs(d)
	p=soup.find("p")
	temp=p.text
	temp=re.sub(r'\[.*\]',"",temp)
	return temp
import urllib2
import pymongo
import re
client=pymongo.MongoClient()
db=client.brainse
political_party=db.politcal_party
l=[]
disp=[]
dic={}
from bs4 import BeautifulSoup as bs
url="https://en.wikipedia.org/wiki/List_of_political_parties_in_India"
data=urllib2.urlopen(url).read()
data=data.split('<table class="wikitable sortable">')
for i in range(3,len(data)):
	data=data[i]
	data=data.split("</table>",1)
	data=data[0]
	soup=bs(str(data))
	tr=soup.findAll("tr")
	print tr[0]
	soup1=bs(str(tr[0]))
	tr=tr[1:]
	th=soup1.findAll("th")
	for i in th:
		l.append(i.text.replace("\n"," "))
	#del l[0]
	print l
	for i in tr:
		soup2=bs(str(i))
		td=soup2.findAll("td")
		k=0
		for j in range(0,len(td)):
			a=td[j].text.replace("\n"," ")
			try:
				a=a[:a.index("[")]
			except:
				pass
			if len(a)>0:
				dic[l[k]]=" "+a+" "
				disp.append(l[k])
			if l[k]=="Name":
				soup3=bs(str(td[j]))
				a=soup3.find("a")
				dic["Link"]=" https://en.wikipedia.org"+a.get("href")+" "
				dic["Description"]=" "+getDesc(dic["Link"])+" "
			if l[k]=="Symbol":
				try:
					soup3=bs(str(td[j]))
					img=soup3.find("img")
					img=img.get("src")[2:]
					dic["Image"]=" "+img+" "
					disp.append("Image")
				except:
					pass
			k=k+1
		disp.append("Description")
		disp.append("Link")
		dic["display_order"]=disp
		print dic
		political_party.insert(dic)
		dic={}
		disp=[]
