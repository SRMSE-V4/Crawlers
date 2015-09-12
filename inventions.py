import urllib2
from bs4 import BeautifulSoup as bs

proxy=urllib2.ProxyHandler({})
opener=urllib2.build_opener(proxy)
opener.addheaders=[('User-agent','Mozilla/5.0')]
urllib2.install_opener(opener)
import pymongo 
client =pymongo.MongoClient()
db=client['inventions_db']


fobj = open("inv.txt","r").read()
url = urllib2.urlopen("http://kalyan-city.blogspot.in/2010/09/inventions-discoveries-list-who.html").read()
soup = bs(url)
div = soup.find("div",{"class":"post"}) 
p = div.findAll("p")
dic={}\7
for i in p:
	try:
		text=i.getText()
		invention,text1=text.split(",",1)
		#print Invention
		#print text1
		invention=filter(lambda t: ord(t)>31 and ord(t)<128,invention)
		dic.update({"Invention":" "+str(invention.strip())+" "})	
		date,text2 =text1.split(".",1)
		if 'c' not in date:
			#print date
			#print text2
			dic.update({"Date":" "+str(date.strip())+" "})
		else:
			date,text2 = text2.split(".",1)
			dic.update({"Date":" "+str(date.strip())+" "})
			#print date
			#print text2 
		text2=text2.split(":",1)
		inventor,extra = text2[1].split(").",1)
		inventor = filter(lambda t: ord(t)>31 and ord(t)<128,inventor)
		dic.update({"Inventor":" "+str(inventor.strip())+") "})
		extra = filter(lambda t: ord(t)>31 and ord(t)<128,extra)
		dic.update({"Extra":" "+str(extra.strip())+" "})

		dic.update({"Display_order":"['Invention','Inventor','Date','Extra']"})
		
		try:
			dic.pop("_id")
		except:
			pass
		print (dic)
		db.inventions.insert(dic)

	except Exception as e:
		print e
		
	print "*************************************"
print 
print "done"