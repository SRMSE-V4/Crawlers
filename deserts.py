from bs4 import BeautifulSoup as bs
from selenium import webdriver
import urllib2
import pymongo
client = pymongo.MongoClient()
db = client['deserts_db'] 
url = urllib2.urlopen("https://en.wikipedia.org/wiki/List_of_deserts_by_area").read()
dic={}
soup = bs(url)
tbl = soup.find("table",{"class":"sortable wikitable"})
tr = tbl.findAll("tr")
for i in range(1,len(tr)):
	td = tr[i].findAll("td")
	
	dic["Rank"] = " "+td[0].getText()+" "
	dic["Link"] = " https://en.wikipedia.org"+td[1].find("a").get("href")+" "
	dic["Name"] = " "+td[1].getText()+" "
	dic["Type"] = " "+td[2].getText()+" "
	dic["Image"] = " https://en.wikipedia.org"+td[3].find("a",{"class":"image"}).get("href")+" "
	dic["Area"] = " "+td[4].find("span",{"style":"display:none"}).getText()+" "
	dic["Location"]= " "+td[6].getText()
	dic["display_order"] = str(["Name","Type","Location","Area","Rank","Image","Link"]) 
	try:
		dic.pop("_id")
	except:
		pass
	db.deserts.insert(dic)
	print dic
	print"******************************************************"
