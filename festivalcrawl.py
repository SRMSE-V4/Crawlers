import MySQLdb
import datetime
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import urllib2
today=datetime.date.today()
y=str(today.year)
client=MongoClient()
db=client.brainse
conn=MySQLdb.connect("localhost","user","pwd","dbname")
co=conn.cursor()
sql="SELECT * FROM `festival`;"
co.execute(sql)
res=co.fetchall()
for i in res:
	l=str(i[2]).replace("2015",y)
	print l
	d=urllib2.urlopen(l).read()
	dic={}
	try:
		soup=bs(d)
		datediv=soup.find("div",class_="festDateNum")
		datediv=str(datediv).split(">",1)
		datediv=datediv[1]
		datediv=datediv.split("<",1)
		datediv=str(datediv[0])
		dic["date"]=datediv
		monthdiv=soup.find("div",class_="festDateTxt")
		monthdiv=str(monthdiv.text).replace(y,"")
		monthdiv=monthdiv.split()
		dic["month"]=str(monthdiv[0])
		dic["day"]=str(monthdiv[1]).replace("(","").replace(")","")
		db.festivals.update({"name":str(i[1])},{"$set":{"date":int(dic["date"])}})
		db.festivals.update({"name":str(i[1])},{"$set":{"month":str(dic["month"])}})
		db.festivals.update({"name":str(i[1])},{"$set":{"day":str(dic["day"])}})
		db.festivals.update({"name":str(i[1])},{"$set":{"day":str(dic["day"])}})
		db.festivals.update({"name":str(i[1])},{"$set":{"link":str(l)}})
	except:
		try:
			d=d.split('<table class="festInnerTbl" >',1)
			d=d[1]
			d=d.split("</table>")
			d=d[0]
			soup=bs(str(d))
			tr=soup.find("tr")
			soup1=bs(str(tr))
			td=soup1.findAll("td")
			dic["date"]=str(td[0].text).strip()
			dic["month"]=str(td[1].text).strip()
			dic["day"]=str(td[2].text).strip().replace("(","").replace(")","")
			db.festivals.update({"name":str(i[1])},{"$set":{"date":str(dic["date"])}})
			db.festivals.update({"name":str(i[1])},{"$set":{"month":str(dic["month"])}})
			db.festivals.update({"name":str(i[1])},{"$set":{"link":str(l)}})
		except:
			pass
