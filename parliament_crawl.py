import urllib2
import re
import sys
import pymongo
client=pymongo.MongoClient("192.168.101.5")
db=client.kbnew
parliaments=db.parliaments
l=[]
disp=[]
final=[]
dic={}
from bs4 import BeautifulSoup as bs
d=urllib2.urlopen("https://en.wikipedia.org/wiki/List_of_legislatures_by_country").read()
d=d.split('<table class="sortable wikitable">')
d=d[3]
d=d.split('</table>',1)
d=d[0]
soup=bs(str(d))
tr=soup.findAll("tr")
soup1=bs(str(tr[0]))
th=soup1.findAll("th")
for i in th:
	l.append(i.text)
print l
tr=tr[1:]
i=0
z=0
ctr=0
while(i<len(tr)):
	soup=bs(str(tr[i]))
	td=soup.findAll("td")
	rowspan=td[0].get("rowspan")
	if rowspan=="2":
		try:
			dic={}
			k=0
			dic[l[k]]=" "+td[0].text+" "
			disp.append(l[k])
			k=k+1
			t=td[1].text
			if len(t)>0:
				t=re.sub(r'\[.*\]','',t)
				dic[l[k]]=" "+t+" "
				ctr=1
				disp.append(l[k])
			k=k+1
			td=td[2:]
			for n in td:
				if len(n.text)>0:
					t=re.sub(r'\[.*\]','',n.text)
					dic[l[k]]=" "+t+" "
					disp.append(l[k])
				k=k+1
			dic["display_order"]=disp
			print dic
			parliaments.insert(dic)
			#final.append(dic)
			print "ok"
			try:
				dic.pop("_id")
			except Exception as e:
				print e
			disp=[]
			disp.append(l[0])
			if ctr==1:
				disp.append(l[1])
			i=i+1
			soup1=bs(str(tr[i]))
			td=soup1.findAll("td")
			k=2
			for n in td:
				if len(n.text)>0:
					t=re.sub(r'\[.*\]','',n.text)
					dic[l[k]]=" "+t+" "
					disp.append(l[k])
				k=k+1
			dic["display_order"]=disp
			print dic
			parliaments.insert(dic)
			dic={}
			print "here"
			#final.append(dic)
			disp=[]
		except Exception as e:
			print e
			dic={}
			
	if not rowspan:
		dic={}
		disp=[]
		try:
			k=0
			for m in td:
				if len(m.text)>0:
					t=re.sub(r'\[.*\]','',m.text)
					dic[l[k]]=" "+t+" "
					disp.append(l[k])
				k=k+1
			dic["display_order"]=disp
			print dic
			parliaments.insert(dic)
			#final.append(dic)
			disp=[]
		except:
			z=z+1
	i=i+1
'''print z
print len(final)	
for i in range(0,len(final)):
	final[i]["_id"]=i
	parliaments.insert(final[i])'''	
				
