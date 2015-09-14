import urllib2
import pymongo
client=pymongo.MongoClient("192.168.101.5")
db=client.kbnew
acts=db.acts
l=[]
dic={}
from bs4 import BeautifulSoup as bs
d=urllib2.urlopen("https://en.wikipedia.org/wiki/List_of_Acts_of_the_Parliament_of_India").read()
d=d.split('<table class="wikitable sortable">')
for m in range(9,len(d)):
	d=d[m]
	d=d.split("</table>",1)
	d=d[0]
	soup=bs(str(d))
	tr=soup.findAll("tr")
	soup1=bs(str(tr[0]))
	th=soup1.findAll("th")
	for i in th:
		x=i.text.replace(".","")
		if x=="Name of the Act":
			x="Name"
		l.append(x)
	print l
	tr=tr[1:]
	for i in tr:
		soup1=bs(str(i))
		td=soup1.findAll("td")
		k=0
		for j in td:
			dic[l[k]]=j.text
			k=k+1
		dic["display_order"]=l;
		print dic
		acts.insert(dic)
		dic={}
