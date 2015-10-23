def crawl(u):
	try:
		dic={}
		url=str(u)
		dic["Link"]=url
		page=urllib2.urlopen(url).read()
		d=page
		d=page.split("<title>",1)
		d=d[1]
		d=d.split("</title>",1)
		d=d[0]
		d=d.split(" - ",1)
		name=d[0].strip()
		dic["Name"]=name
		data=page.split('<table class="plDetail">',1)
		data=data[1]
		data=data.split("</table>",1)
		data=data[0]
		soup=bs(str(data))
		data1=soup.find_all("td")
		imgtd=str(data1[0])
		imgtd=imgtd.split('src="',1)
		imgtd=imgtd[1]
		imgtd=imgtd.split('"',1)
		image="http://www.tennisexplorer.com"+str(imgtd[0])
		dic["Image"]=image
		soup1=bs(str(data1))
		div=soup1.findAll("div",class_="date")
		for i in div:
			a=i.text
			a=a.split(":",1)
			dic[a[0].title()]=a[1].title()
		if dic.has_key("Current/Highest Rank - Singles"):
			d1=str(dic["Current/Highest Rank - Singles"])
			if "- / " in d1:
				d1=d1.split("- / ")
				dic.pop("Current/Highest Rank - Singles")
				if len(d1[0].replace(".","").strip())!=0:
					dic["Current Rank - Singles"]=str(d1[0]).replace(".","").strip()
				if len(str(d1[1]).replace(".","").strip())!=0:
					dic["Highest Rank - Singles"]=str(d1[1]).replace(".","").strip()
			elif " / " in d1:
				d1=d1.split(" / ")
				dic.pop("Current/Highest Rank - Singles")
				if len(d1[0].replace(".","").strip())!=0:
					dic["Current Rank - Singles"]=str(d1[0]).replace(".","").strip()
				if len(str(d1[1]).replace(".","").strip())!=0:
					dic["Highest Rank - Singles"]=str(d1[1]).replace(".","").strip()
			elif " - / " in d1:
				d1=d1.split(" - / ")
				dic.pop("Current/Highest Rank - Singles")
				if len(d1[0].replace(".","").strip())!=0:
					dic["Current Rank - Singles"]=str(d1[0]).replace(".","").strip()
				if len(str(d1[1]).replace(".","").strip())!=0:
					dic["Highest Rank - Singles"]=str(d1[1]).replace(".","").strip()
			elif ". / " in d1:
				d1=d1.split(". / ")
				dic.pop("Current/Highest Rank - Singles")
				if len(d1[0].replace(".","").strip())!=0:
					dic["Current Rank - Singles"]=str(d1[0]).replace(".","").strip()
				if len(str(d1[1]).replace(".","").strip())!=0:
					dic["Highest Rank - Singles"]=str(d1[1]).replace(".","").strip()
			else:
				d1=d1.replace(".","").strip()
				dic.pop("Current/Highest Rank - Singles")
				if len(d1.replace(".","").strip())!=0:
					dic["Highest Rank - Singles"]=str(d1).replace(".","").strip()
		if dic.has_key("Current/Highest Rank - Doubles"):
			df=str(dic["Current/Highest Rank - Doubles"])
			if "- / " in df:
				df=df.split("- / ")
				dic.pop("Current/Highest Rank - Doubles")
				if len(df[0].replace(".","").strip())!=0:
					dic["Current Rank - Doubles"]=str(df[0]).replace(".","").strip()
				if len(df[1].replace(".","").strip())!=0:
					dic["Highest Rank - Doubles"]=str(df[1]).replace(".","").strip()
			elif " / " in df:
				df=df.split(" / ")
				dic.pop("Current/Highest Rank - Doubles")
				if len(df[0].replace(".","").strip())!=0:
					dic["Current Rank - Doubles"]=str(df[0]).replace(".","").strip()
				if len(df[1].replace(".","").strip())!=0:
					dic["Highest Rank - Doubles"]=str(df[1]).replace(".","").strip()
			elif " - / " in df:
				df=df.split(" - / ")
				dic.pop("Current/Highest Rank - Doubles")
				if len(df[0].replace(".","").strip())!=0:
					dic["Current Rank - Doubles"]=str(df[0]).replace(".","").strip()
				if len(df[1].replace(".","").strip())!=0:
					dic["Highest Rank - Doubles"]=str(df[1]).replace(".","").strip()
			elif ". / " in df:
				df=df.split(". / ")
				dic.pop("Current/Highest Rank - Doubles")
				if len(df[0].replace(".","").strip())!=0:
					dic["Current Rank - Doubles"]=str(df[0]).replace(".","").strip()
				if len(df[1].replace(".","").strip())!=0:
					dic["Highest Rank - Doubles"]=str(df[1]).replace(".","").strip()
			else:
				df=df.replace(".","").strip()
				dic.pop("Current/Highest Rank - Doubles")
				if len(df.replace(".","").strip())!=0:
					dic["Highest Rank - Doubles"]=str(df).replace(".","").strip()
		tennis1.insert(dic)
	except:
		pass
import urllib2
import MySQLdb
import pymongo
import threading
T = threading.Thread
from bs4 import BeautifulSoup as bs
c = pymongo.Connection()
c['dbname'].drop_collection('tennis1')
client=pymongo.MongoClient("ip")
db=client.dbname
tennis1=db.tennis1
conn=MySQLdb.connect("localhost","user","pwd","dbname")
co=conn.cursor()
sql="SELECT `link` from `tennis`;"
co.execute(sql)
res=co.fetchall()
for r in res:
	u=str(r[0])
	while threading.active_count()>200:
		continue
	t = T(target=crawl,args=(u,))
	t.start()
	
	
