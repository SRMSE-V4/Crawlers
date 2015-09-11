#x=filter(lambda x:ord(x)>31 and ord(x)<128,i.text)
import pymongo
import urllib2
from bs4 import BeautifulSoup

client=pymongo.MongoClient()
mdb=client['brainse']
qb=mdb['mountains']

def process_table(tb1):
	#print "here"
	rdata={}
	row=tb1.find_all("tr")
	del row[0]
	for i in row:
		data=i.find_all("td")
		#print data
		rdata["Name"]=" "+data[0].find('a').get_text()+" "
		if data[0].find("a")!=None:
			rdata["Link"]=" https://en.wikipedia.org"+data[0].find("a").get('href')+" "
		rdata["Metres"]=" "+data[1].get_text()+" "
		rdata["Feet"]=" "+data[2].get_text()+" "
		x=filter(lambda x:ord(x)>31 and ord(x)<128,data[3].get_text())
		rdata["Range"]=" "+str(x)+" "
		x=filter(lambda x:ord(x)>31 and ord(x)<128,data[4].get_text())
		rdata["Location and Description"]=" "+str(x)+" "
		#print data[0]
		#rdata["Name"]=data[0].find('a').get_text()
		print rdata["Name"]
		#count=count+1	

def process_table1(tb):
	rdata={}
	row=tb.find_all("tr")
	del row[0]
	for i in row:
		data=i.find_all("td")
		#print data
		if data[0].find('a')!=None:
			rdata["Name"]=" "+data[0].find('a').get_text()+" "
		else:
			rdata["Name"]=" "+str(data[0].get_text())+" "
		if data[0].find("a")!=None:
			rdata["Link"]=" https://en.wikipedia.org"+data[0].find("a").get('href')+" "
		rdata["Metres"]=" "+data[1].get_text()+" "
		rdata["Feet"]=" "+data[2].get_text()+" "
		x=filter(lambda x:ord(x)>31 and ord(x)<128,data[3].get_text())
		rdata["Location and Description"]=" "+str(x)+" "
		print rdata["Name"]
rdata={}
count=0
url="https://en.wikipedia.org/wiki/List_of_mountains_by_elevation"
pg=urllib2.urlopen(url).read()
pg=pg.replace("&#160;&#160","")
soup=BeautifulSoup(pg)
tb=soup.find_all("table",class_="wikitable sortable")
process_table(tb[0])
tb1=soup.find_all("table",class_="sortable wikitable")
process_table(tb1[0])
process_table(tb1[2])
process_table1(tb1[1])
process_table1(tb1[3])
process_table1(tb1[4])
process_table1(tb1[5])
process_table1(tb1[6])
process_table1(tb1[7])
