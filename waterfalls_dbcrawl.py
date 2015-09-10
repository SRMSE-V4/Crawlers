from bs4 import BeautifulSoup as bs
import urllib2
import pymongo
client=pymongo.MongoClient()
db=client.brainse
waterfalls=db.waterfalls
for k in range(1,20):
	url="http://www.worldwaterfalldatabase.com/tallest-waterfalls/total-height/"+str(k)+"/"
	d=urllib2.urlopen(url).read()
	d=d.rsplit('<table width="100%" border="0" cellpadding="5" cellspacing="1" class="sideBarTableAlignment">',1)
	d=d[1]
	d=d.split("</table>",1)
	d=d[0]
	soup=bs(str(d))
	l=[]
	disp=[]
	dic={}
	tr=soup.findAll("tr")
	for j in range(2,len(tr)-1):
		soup1=bs(str(tr[j]))
		td=soup1.findAll("td")
		for i in range(0,len(td)):
			if i==4 or i==5:
				continue
			if i==0:
				rank=" "+td[i].text
				dic["Rank"]=rank[:rank.index("\t")]+" "
				disp.append("Rank")
			elif i==1:
				dic["Name"]=" "+td[i].text.strip()+" "
				disp.append("Name")
				soup2=bs(str(td[i]))
				a=soup2.find("a")
				dic["Link"]=" http://www.worldwaterfalldatabase.com"+a.get("href")+" "
			elif i==2:
				l.append(" "+td[i].text.strip()+" ")
			elif i==3:
				l.append(" "+td[i].text.strip()+" ")
				dic["Height"]=l
				disp.append("Height")
				l=[]
			elif i==6:
				state=td[i].text.strip()
				if len(state)>2:
					dic["State/Province"]=" "+state+" "
					disp.append("State/Province")
			elif i==7:
				dic["Country"]=" "+td[i].text.strip()+" "
				disp.append("Country")
		disp.append("Link")
		dic["display_order"]=disp
		disp=[]
		print dic
		waterfalls.insert(dic)
		dic={}
	print str(k)+" page completed"
