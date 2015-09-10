import urllib2
import pymongo
client=pymongo.MongoClient()
db=client.brainse
wonders_world=db.wonders_world
from bs4 import BeautifulSoup as bs
rank=1
url="https://en.wikipedia.org/wiki/New7Wonders_of_the_World"
d=urllib2.urlopen(url).read()
d=d.split('<table class="wikitable">',1)
d=d[1]
d=d.split("</table>",1)
d=d[0]
dic={}
soup=bs(str(d))
tr=soup.findAll("tr")
for i in range(1,len(tr)):
	soup1=bs(str(tr[i]))
	td=soup1.findAll("td")
	for j in range(0,len(td)):
		if j==0:
			name=" "+td[j].text
			dic["Name"]=name[:name.index("\n")]+" "
			soup2=bs(str(td[j]))
			a=soup2.find("a")
			l="https://en.wikipedia.org/"+a.get("href")
			dic["Link"]=" "+filter(lambda x:ord(x)>31 and ord(x)<128,l)+" "
		elif j==1:
			dic["Location"]=" "+filter(lambda x:ord(x)>31 and ord(x)<128,td[j].text)+" "
		elif j==2:
			soup2=bs(str(td[j]))
			img=soup2.find("img")
			dic["Image"]=" "+img.get("src")[2:].replace("100px","300px")+" "
		elif j==3:
			dic["Year"]=" "+filter(lambda x:ord(x)>31 and ord(x)<128,td[j].text)+" "
			dic["display_order"]=["Rank","Name","Location","Year","Built By","Image"]
	if dic["Name"]==" Great Wall of China ":
		dic["Built By"]=" Soldiers, Common People and Criminals "
	elif dic["Name"]==" Great Pyramid of Giza ":
		dic["Built By"]=" Khufu, Imhotep, Hemiunu "
	elif dic["Name"]==" The Colosseum ":
		dic["Built By"]=" Vespasian, Titus "
	elif dic["Name"]==" Taj Mahal ":
		dic["Built By"]=" Ustad Ahmad Lahouri, Ustad Isa "
	elif dic["Name"]==" Christ the Redeemer ":
		dic["Built By"]=" Paul Landowski, Heitor da Silva Costa, Albert Caquot "
	elif dic["Name"]==" Machu Picchu ":
		dic["Built By"]="  Pachacutec Inca Yupanqui and Tupac Inca Yupanqui "
	elif dic["Name"]==" Petra ":
		dic["Built By"]=" Ancient Civilization "
	dic["Rank"]=" "+str(rank)+" "
	rank=rank+1
	print dic
	wonders_world.insert(dic)
	dic={}
