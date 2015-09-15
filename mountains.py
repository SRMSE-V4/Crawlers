#crawler for crawling world mountains from wikipedia
import pymongo
import urllib2
from bs4 import BeautifulSoup

client=pymongo.MongoClient()
mdb=client['brainse']
qb=mdb['mountains']

def image_search(rdata):
	link=rdata["Link"]
	pg=urllib2.urlopen(link).read()
	soup=BeautifulSoup(pg)
	info=soup.find("table",class_="infobox vcard")
	img=info.find_all("img")
	if len(img)!=0:
		rdata["display_order"].append("Image")
		rdata["Image"]=" https:"+img[0].get('src')+" "
		#print rdata["Image"]
		return rdata
	else:
		return rdata
		
#function for processing table 1 and 3
def process_table(tb1):
	row=tb1.find_all("tr")
	del row[0]
	for i in row:
		try:
			rdata={}
			data=i.find_all("td")
			rdata["Name"]=" "+data[0].find('a').get_text()+" "
			if data[0].find("a")!=None:
				rdata["Link"]=" https://en.wikipedia.org"+data[0].find("a").get('href')+" "
			rdata["Metres"]=" "+data[1].get_text()+" "
			rdata["Feet"]=" "+data[2].get_text()+" "
			x=filter(lambda x:ord(x)>31 and ord(x)<128,data[3].get_text())
			rdata["Range"]=" "+str(x)+" "
			rdata["Range"]=rdata["Range"].replace(";","")
			x=filter(lambda x:ord(x)>31 and ord(x)<128,data[4].get_text())
			rdata["Location and Description"]=" "+str(x)+" "
			rdata["display_order"]=["Name","Metres","Feet","Range","Location and Description","Link"]
			print rdata["Name"]
			rdata=image_search(rdata)
			qb.insert(rdata)
		except Exception as e:
			print e
			pass
			
#function for processing rest of the tables excluding the last one
def process_table1(tb):
	row=tb.find_all("tr")
	del row[0]
	for i in row:
		try:
			rdata={}
			data=i.find_all("td")
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
			rdata["display_order"]=["Name","Metres","Feet","Location and Description","Link"]
			print rdata["Name"]
			rdata=image_search(rdata)
			qb.insert(rdata)
		except Exception as e:
			print e
			pass

#function for crawling last table
def process_table2(tb):
	row=tb.find_all("tr")
	del row[0]
	for i in row:
		try:
			rdata={}
			data=i.find_all("td")
			if data[0].find('a')!=None:
				rdata["Name"]=" "+data[0].find('a').get_text()+" "
			else:
				rdata["Name"]=" "+str(data[0].get_text())+" "
			if data[0].find("a")!=None:
				rdata["Link"]=" https://en.wikipedia.org"+data[0].find("a").get('href')+" "
			rdata["Metres"]=" "+data[1].get_text()+" "
			rdata["Feet"]=" "+data[2].get_text()+" "
			x=filter(lambda x:ord(x)>31 and ord(x)<128,data[4].get_text())
			rdata["Location and Description"]=" "+str(x)+" "
			rdata["display_order"]=["Name","Metres","Feet","Location and Description","Link"]
			print rdata["Name"]
			rdata=image_search(rdata)
			qb.insert(rdata)
		except Exception as e:
			print e
			pass

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
process_table2(tb1[7]) 
