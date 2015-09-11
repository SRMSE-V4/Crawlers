import pymongo
import urllib2
from bs4 import BeautifulSoup

client=pymongo.MongoClient()
mdb=client['brainse']
qb=mdb['chiefjustice']

url="https://en.wikipedia.org/wiki/List_of_Chief_Justices_of_India"
pg=urllib2.urlopen(url).read()
soup=BeautifulSoup(pg)
tb=soup.find("table",class_="sortable wikitable")
row=tb.find_all("tr",align="center")
pres=""
rdata={}
num=0
for i in row:
	data=i.find_all("td")
	name_t=data[1]
	name_t=name_t.find("a")
	rdata["display_order"]=["Name","Link","Starting Date","Ending Date","Length of Term","Bar","Appointed By"]
	rdata["Name"]=" "+str(name_t.get_text())+" "
	rdata["Link"]=" https://en.wikipedia.org"+str(name_t.get('href'))+" "
	date_i=data[2].find("span",style="white-space:nowrap").get_text()
	date_f=data[3].find("span",style="white-space:nowrap")
	if date_f!=None:
		date_f=date_f.get_text()
	else:
		date_f="Incumbent"
	rdata["Starting Date"]=" "+str(date_i)+" "
	rdata["Ending Date"]=" "+str(date_f)+" "
	tlen=data[4].get_text()
	rdata["Length of Term"]=" "+tlen+" "
	bar=data[5].find("a").get_text()
	rdata["Bar"]=" "+bar+" "
	if pres == "" and num==0:
		pres=data[6]
		if pres.get('rowspan')!=None:
			num=int(pres.get('rowspan'))
			pres_name=pres.find("a").get_text()
			num=num-1;
			rdata["Appointed By"]=" "+str(pres_name)+" "
			
		else:
			pres_name=pres.find("a").get_text()
			rdata["Appointed By"]=" "+str(pres_name)+" "
	else:
		rdata["Appointed By"]=" "+str(pres_name)+" "
		num=num-1
	if num==0:
		pres=""
	url1=rdata["Link"]
	pg1=urllib2.urlopen(url1).read()
	sp=BeautifulSoup(pg1)
	tb=sp.find("table",class_="infobox vcard")
	img=tb.find("img")
	if img!=None:
		rdata["Image"]=" https://"+str(img.get('src'))+" "
		rdata["display_order"].append("Image")
	print rdata["Name"]
	qb.insert(rdata)
	rdata={}
