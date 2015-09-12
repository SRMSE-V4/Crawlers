import urllib2 
from bs4 import BeautifulSoup as bs
import pymongo
client = pymongo.MongoClient()
db=client['islands_db']

proxy=urllib2.ProxyHandler({})
opener=urllib2.build_opener(proxy)
opener.addheaders=[('User-agent','Mozilla/5.0')]
urllib2.install_opener(opener)

url = urllib2.urlopen("https://en.wikipedia.org/wiki/List_of_islands_by_area").read()
soup = bs(url)
div = soup.find("div",{"id":"mw-content-text"})
table =  div.findAll("table")
ct=0
for i in range(1,len(table)-1):

	tr = table[i].findAll("tr")
	for j in range(1,len(tr)):
		dic={}
		display_list=["Island's name","Country","Area","Island's url"]
		td =tr[j].findAll("td")
		if ct<177:
			#print td[1].find("a").get("href")
			
			dic["Island's name"] = " "+td[1].find("a").getText().strip()+" "
			dic["Island's url"] = " https://en.wikipedia.org"+td[1].find("a").get("href")+" "
			dic["Area"] = " "+td[3].getText().strip()+" (sq mi) "
			country_temp = filter(lambda t : ord(t)>31 and ord(t)<128,td[4].getText() )
			dic["Country"] =" "+country_temp.strip()+" "
			
		
			

		else :
			
			dic["Island's name"] = " "+td[0].find("a").getText().strip()+" "
			dic["Island's url"] = " https://en.wikipedia.org"+td[0].find("a").get("href")+" "
			country_temp = td[3].getText()
			if "None" in country_temp:
				country_temp = country_temp.split("(")
				country_temp = country_temp[1].split(")")
				country_temp = country_temp[0]
				dic["Country"] = " "+country_temp.strip()+" "
			else:
				dic["Country"] =" "+td[3].getText().strip()+" "
		#print dic
		try:
			
			urlnew = urllib2.urlopen(dic["Island's url"]).read()
			
			soupnew = bs(urlnew)
			try:
				tbl = soupnew.find("table",{"class":"infobox vcard"})
				trnew = tbl.findAll("tr")
				image_list=[]

				for row in trnew:
					if row.find("td",{"style":"text-align:center"}):
						
						tdnew = row.find("td",{"style":"text-align:center"})
						if tdnew.find("a",{"class":"image"}):
							#print td.find("a",{"class":"image"}).get("href")
							image_list.append("https://en.wikipedia.org"+tdnew.find("a",{"class":"image"}).get("href"))
							#print image_list
					dic.update({"Image":str(image_list)})
					if row.find("th",{"scope":"row"}):
						thnew = row.find("th",{"scope":"row"}).getText()
						thnew = filter(lambda t : ord(t)>31 and ord(t)<128, thnew)

						try : 
							if thnew == 'Area' or thnew =='Population' or thnew == 'Density':
							
								if thnew == 'Area':
									if 'Area' in dic.keys():
										dic.pop("Area")                  #inserting the refine Area size 
										tdnew = row.find("td").getText()
										tdnew = tdnew.split("[")
										tdnew = tdnew[0].split("(")
										dic.update({thnew:" "+tdnew[0].replace(u'\xa0', u' ').strip()+" "})
								
								tdnew = row.find("td").getText()
								tdnew = tdnew .split("[")
								
								tdnew = tdnew[0].split("(")
						
								dic.update({thnew:" "+tdnew[0].replace(u'\xa0', u' ').strip()+" "})
						 		
						except Exception as e:
							print e
							
						
			except Exception as e:
				print e
			if "Population" in dic.keys():
				display_list.append("Population")
			if "Density" in dic.keys():
				display_list.append("Density")
			dic["Display_order"]=str(display_list)
			
			try:
				dic.pop("_id")
			except:
				pass
			print (dic)
			db.islands.insert(dic)
			
			print "********************************************************"
			print ct

		except :
			pass
		ct+=1

				
	
