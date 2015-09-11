def findtable(url,country):
	print url
	print country
	dic={}
	l=[]
	key=[]
	#key.append("Earthquake")
	data=urllib2.urlopen(url).read()
	data=data.split('<table class="wikitable sortable">')
	data=data[1]
	data=data.split("</table>",1)
	data=data[0]
	soup=bs(str(data))
	tr=soup.findAll("tr")
	soup3=bs(str(tr[0]))
	th=soup.findAll("th")
	for i in th:
		x=filter(lambda x:ord(x)>31 and ord(x)<128,i.text)
		if x=="M":
			x="Magnitude"
		elif x=="MM":
			x="Intensity"
		elif x=="MMI":
			x="Intensity"
		elif x=="Date[1]":
			x="Date"
		elif x=="Nameofquake":
			x="Earthquake"
		elif x=="Rmajiname":
			x="Romaji Name"
		elif x=="Japanesename":
			x="Japanese Name"
		elif x=="Lat.":
			x="Latitude"
		elif x=="Long.":
			x="Longitude"
		elif x=="Housesdestroyed":
			x="Houses Destroyed"
		elif x=="Magnitude(ML":
			x="Magnitude(ML)"
		elif x=="PTZ":
			x="Pacific Time Zone"
		elif x=="Lat":
			x="Latitude"
		elif x=="Long":
			x="Longitude"
		key.append(x)
	#del key[1]
	del key[len(key)-1]
	print key
	for i in range(1,len(tr)):
		soup1=bs(str(tr[i]))
		td=soup1.findAll("td")
		k=0
		for j in range(0,len(td)-1):
			try:
				temp=td[j].text
				try:	
					temp=td[j].text[:temp.index("[")]
				except:
					pass
				if len(temp)>0:
					if key[k]=="Date":
						try:
							t1=temp
							temp=filter(lambda x:ord(x)>31 and ord(x)<128,temp)
							temp=temp.split("-0000",1)
							temp=str(temp[1])
						except Exception as e:
							print e
							temp=t1
					elif key[k]=="Place":
						try:
							a1=temp
							temp=temp.split("see ",1)
							temp=str(temp[0])
							temp=temp.replace("\n","")
						except:
							temp=a1
					dic[key[k]]=" "+temp+" "
					l.append(key[k])
			except:
				pass
			k=k+1
		dic["Country"]=" "+str(country)+" "
		l.append("Country")
		dic["display_order"]=l			
		print dic
		earthquakes.insert(dic)
		l=[]
		dic={}	
link=[]
name=[]
import urllib2
import pymongo
client=pymongo.MongoClient()
db=client.brainse
earthquakes=db.earthquakes
from bs4 import BeautifulSoup as bs
d=urllib2.urlopen("https://en.wikipedia.org/wiki/Lists_of_earthquakes").read()
d=d.split('<div class="div-col columns column-count column-count-4" style="-moz-column-count: 4; -webkit-column-count: 4; column-count: 4;">',1)
d=d[1]
d=d.split("</div>")
d=d[0]
soup=bs(str(d))
li=soup.findAll("li")
for i in li:
	soup1=bs(str(i))
	a=soup1.find("a")
	name.append(a.text)
	link.append("https://en.wikipedia.org"+a.get("href"))
findtable(link[50],name[50])
