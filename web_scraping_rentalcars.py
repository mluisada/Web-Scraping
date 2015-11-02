############################################
#   Web-scraping for educational purposes  #
#      	   Website : rentalcars       	   # 
#              February 2015               #
#                                          #
#           LUISADA Marie-Laura            #
############################################


## N.B. I used this data as a learning tool, for educational purposes only, not for commercial goals.


# coding:utf-8  -- to be able to write '€' symbol

## import useful modules
import requests
from bs4 import BeautifulSoup
import csv


## Create csv file
f = csv.writer(open("rentalcars.csv","w"))
# Write headers on the first row
f.writerow(["type", "company", "car", "price", "rating"])



## Data scraping from rentalcars.com

# Where ? San Francisco CA, USA. When ? Btw January 25th and 28th
url = "http://www.rentalcars.com/SearchResults.do?dropCity=San+Francisco&doMinute=30&location=4189&driversAge=30&doHour=11&searchType=&locationName=San+Francisco+Airport&doFiltering=false&puSameAsDo=on&city=San+Francisco&puHour=11&dropCountryCode=&dropCountry=USA+-+California&puDay=25&filterTo=1000&dropLocation=4189&driverage=on&doDay=28&countryCode=&dropLocationName=San+Francisco+Airport&country=USA+-+California&enabler=&filterFrom=0&puMonth=1&puMinute=30&doMonth=1&doYear=2015&puYear=2015&fromLocChoose=true&filterName=CarCategorisationSupplierFilter"


# Create the related html page
html_doc = requests.get(url).content


# Use BS module for a better visualization and data exploiting
soup = BeautifulSoup(html_doc)


# Focus on each division which contain info about one specific car
# div is a part of the html code
div = soup.find_all("div", {"class":"car-result group "}) 



# Scan the components of div
	# get info from all paragraphs (name of the car / price)
	# get info from the image (competitor's name)
	# get info in between a span tag (type of car)

		# if the selected locations are not empty:
			# define these observations (name of the car / price etc.)
		# else:
			# the cell will be empty
			# loop again
		# add each observation to a row of the csv file


for item in div:
	pinfo = item.find_all("p")
	pprice = item.find_all("p", {"class":"now "})
	img = item.find_all("img")
	typecar = item.find_all("span",{"class":"class mini"}) #it is a list ==> typecar[0] 
	try: 
	# some versions display ratings, some others don't
		prating = item.find_all("p", {"class":"num"})
	except:
		continue

	try:
		car = str(pinfo[0].get_text())
		price = pprice[0].get_text()
		price = price[:-1] # remove € symbol beacause the csv file refuses it
		price = price.replace(",",".")
		company = str(img[1].get("title"))
		ctype = str(typecar[0].get_text())
		try:
			rating = float(prating[0].contents[0])
		except:
			rating = ""
			continue

	except:
		print ""
		continue
		
	#Add new line
	f.writerow([ctype, company, car, price, rating])


### END
	