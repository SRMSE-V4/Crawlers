from bs4 import BeautifulSoup as bs
import re
from urllib2 import urlopen
import pymongo
import string 
client = pymongo.MongoClient()
db = client['brainse']
#s=bs(open('a.txt','r').read())
for z in string.uppercase:
	lines=['/diseases-conditions/index?letter='+str(z)]
	for line in lines:
		link='http://www.mayoclinic.org'+line
		soup=bs(urlopen(link).read())
		ols=soup.findAll('ol')
		ols=ols[1]
		li=ols.findAll('li')
		c=0
		for l in li:
		    dic={}
		    link2='http://www.mayoclinic.org'+l.find('a').get('href')
		    print '!!!',l.find('a').getText(),'!!!'
		    dic["link"]=str(link2)
		    soup2=bs(urlopen(link2).read())
		    ol_line=soup2.find('ol').findAll('li')
		    x='defination'
		    y=''
		    s=soup2.find('div',id='main-content').findAll('p')
		    for s1 in s:
		        y=y+s1.getText('',strip=True)
		    y=y.replace('At Mayo Clinic, we take the time to listen, to find answers and to provide you the best care.','')
		    y=y.replace('Mayo Clinic is a not-for-profit organization. Make a difference today.','')
		    c=c+1
		    temp={x:y}
		    dic.update(temp)
		    z=0
		    for li in ol_line:
		        if(z>1 and z<6):
		            linkcr='http://www.mayoclinic.org'+li.find('a').get('href')
		            soupcr=bs(urlopen(linkcr).read())
		            soupcr=soupcr.find('div',id="main-content")
		            x=li.getText('',strip=True)
		            if(x=='Preparing for your appointment'):
		                continue
		            y=''
		            divs=soupcr.findAll('div')
		            for div in divs:
		                div.clear()
		            soupcr.find('ul',class_="page content").decompose()
		            soupcr.find('menu',class_='social').decompose()
		            soupcr.find('span',class_='moddate').decompose()
		            y=soupcr.getText('|',strip=True);
		            y=y.replace('|Share|Tweet','')
		            y=y.split('|')
		            temp={x:y}
		            dic.update(temp)
		        z=z+1
		    #print dic
		    db.disease1.save(dic)
