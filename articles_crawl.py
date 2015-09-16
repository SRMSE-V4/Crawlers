def getdetails(url,dic):
	m=[]
	ctr=0
	data=urllib2.urlopen(url).read()
	data=data.split('<h5 style="font-size:13px;font-weight:bold">ARTICLE</h5>')
	for x in range(1,len(data)):
		data1=data[x]
		soup=bs(str(data1))
		h4=soup.findAll("h4",style="font-weight:bold")
		for j in range(1,len(h4)):
			temp=h4[j].text.replace("\n","")
			if len(temp)>0 and temp[0].isdigit()==True:
				try:
					dic.pop("_id")
				except:
					pass
				temp=temp.split(".",1)
				dic["Article Number"]=" "+temp[0]+" "
				dic["Article Name"]=" "+temp[1].strip()+" "
				dic["display_order"]=["Part","Part Name","Article Number","Article Name"]
				print dic
				ctr=ctr+1
				articles.insert(dic)
	if ctr==0:
		f=open("articleserror.txt","a")
		f.write(url)
		f.close()
from bs4 import BeautifulSoup as bs
import urllib2
import pymongo
client=pymongo.MongoClient("192.168.101.5")
db=client.kbnew
articles=db.articles
dic={}
d=urllib2.urlopen("http://www.constitution.org/cons/india/const.html").read()
d=d.split("""<table style="width:702px;background-color:rgba(0,0,0,0);color:#333;border-top-style:none;border-bottom-style:none;border-right-style:none;border-left-style:none;border-top-width:0px;border-bottom-width:0px;border-right-width:0px;border-left-width:0px;border-top-color:gray;border-bottom-color:gray;border-right-color:gray;border-left-color:gray;ez_table_text_min_width:430" cellpadding=2 data-role=table class=ez_wrap_table ezoic=combined data-ez-uid=1340446044 data-ez-gwidth=702>""",1)
d=d[1]
d=d.split("</table>",1)
d=d[0]
soup=bs(str(d))
tr=soup.findAll("tr")
for i in range(0,len(tr)):
	soup1=bs(str(tr[i]))
	td=soup1.findAll("td")
	for j in range(0,len(td)):
		if j==0:
			dic["Part"]=" "+td[j].text+" "
		elif j==1:
			dic["Part Name"]=" "+td[j].text.title().replace("\n"," ").strip()+" "
		elif j==2:
			soup2=bs(str(td[j]))
			a=soup2.find("a")
			link="http://www.constitution.org/cons/india/"+a.get("href")
			print link
			try:
				getdetails(link,dic)
			except:
				f=open("articleserror.txt","a")
				f.write(str(dic))
				f.close()
	dic={}
