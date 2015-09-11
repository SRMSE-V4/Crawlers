#code for scrapping the current judges of supreme court of india
import urllib2
import pymongo

from bs4 import BeautifulSoup
result=[]
details=[]
dump=[]
q={}
img=[]
p_url=[]

client = pymongo.MongoClient()
mdb = client['test']
qb=mdb['judges']

#scrapping image links
url="http://supremecourtofindia.nic.in/judges/judges.htm"
page=urllib2.urlopen(url).read()
soup=BeautifulSoup(page)
tb=soup.find("table",height="3085")
j_img=soup.find_all("img")
del j_img[0]
del j_img[0]


#scrapping profile links
for k in j_img:
	k=k.get('src')
	link="http://supremecourtofindia.nic.in/judges/"+str(k)
	img.append(link)

#scrapping rest of the data from wikipedia 
a_links=soup.find_all("a")
for i in a_links:
	if i.get_text()=="PROFILE":
		p_url.append(str("http://supremecourtofindia.nic.in/judges/"+str(i.get('href'))))
url1="https://en.wikipedia.org/wiki/List_of_sitting_judges_of_the_Supreme_Court_of_India"
page1=urllib2.urlopen(url1).read()
soup1=BeautifulSoup(page1)
tb1=soup1.find("table","wikitable sortable")
tbd=tb1.find_all("td")
count=0
img_ctr=0
for i in tbd:
	count=count+1
	dump.append(i.get_text())
	if (count%4==0):
		dump.append(img[img_ctr])
		dump.append(p_url[img_ctr])
		details.append(dump)
		dump=[]
		img_ctr=img_ctr+1
for j in details:
	q["display_order"]=["Name","Image","Appointed","Retirement Date","Profile Link"]
	q["Name"]=" "+j[1]+" "
	q["Appointed"]=" "+j[2]+" "
	q["Retirement Date"]=" "+j[3]+" "
	q["Image"]=" "+j[4]+" "
	q["Profile Link"]=" "+j[5]+" "
	#result.append(q)
	qb.insert(q)
	#print q
	q={}

#print result		
