import urllib2
from bs4 import BeautifulSoup as bs
import pymongo
client=pymongo.MongoClient("192.168.101.5")
db=client.kbnew
dances=db.dances
l=[]
d=urllib2.urlopen("http://www.quizvook.com/2013/01/dances-of-india-complete-list-latest.html").read()
d=d.split('<table border="10" cellspacing="3" cellpadding="10">',1)
d=d[1]
d=d.split("</table>",1)
d=d[0]
dic={}
soup=bs(str(d))
tr=soup.findAll("tr")
soup1=bs(str(tr[0]))
th=soup.findAll("th")
for i in th:
	l.append(i.text.lower().title());
del l[0]
tr=tr[1:]
print l
for i in tr:
	soup=bs(str(i))
	td=soup.findAll("td")
	dic["State"]=" "+td[2].text+" "
	soup=bs(str(td[1]))
	li=soup.findAll("li")
	for j in li:
		dic["Name"]=" "+j.text+" "
		print dic
		dances.insert(dic)
