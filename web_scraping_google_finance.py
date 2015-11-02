############################################
#     Web-scraping with Beautiful soup     #
#        Website : Google Finance          # 
#              October 2015                #
#                                          #
#           LUISADA Marie-Laura            #
############################################


## N.B. I used this data as a learning tool, for educational purposes only, not for commercial goals.



### IMPORT PACKAGES ###
from bs4 import BeautifulSoup
import urllib.request as ul


### RETRIEVE FIRST HTML PAGE ###
url = "http://www.google.com/finance"
url_response = ul.urlopen(url, timeout = 10)
soup = BeautifulSoup(url_response)


### SELECT TABLE OF SECTORS ###
sect_div = soup.find("div", {"id":"secperf"})
sect_tbl = sect_div.table


### SCRAWL LIST OF SECTORS, LINKS AND RATES ###
sector, rate, link = [], [], []

for row in sect_tbl.find_all('tr'):
    for col in row.find_all('td'):
        # look for sectors and hyperlinks
        if col.a is not None:
            sector.append(col.a.get_text())
            link.append(col.a.get('href'))
        # look for rates
        if col.span is not None:
            temp_rate = col.span.get_text()
            # remove % symbol and convert items to float
            rate.append(float(temp_rate[:-1]))

            
### GET TOP MOVER SECTOR AND RELATED LINK
sect_ind = rate.index(max(rate))
top_sect = sector[sect_ind]
top_link = "http://www.google.com" + link[sect_ind]
    
    
### RETRIEVE SECOND HTML PAGE ###
url_response = ul.urlopen(top_link, timeout = 10)
soup = BeautifulSoup(url_response)
company_tbl = soup.find("table", class_ = "topmovers")


### SCRAWL LIST OF COMPANIES AND RATES ###
company = []
change = []

for row in company_tbl.find_all('tr'):
    for col in row.find_all('td'):
        if col.a is not None:
            company.append(col.a.get_text())
        if col.span is not None:
            # select percentage (not volume) which is the 2nd argument
            temp_chg = col.find_all('span')[1].get_text()
            # remove % and () then convert items to float
            change.append(float(temp_chg[1:-2]))

# select only the names of the companies, not tickers (which immediately follow)
company = company[::2]

### GET TOP / FLOP COMPANIES
winner_ind = change.index(max(change))
loser_ind = change.index(min(change))
winner = company[winner_ind]
loser = company[loser_ind]


### ANNOUNCEMENT
print('The sector that has moved the most is ' + top_sect + ' (' + str(max(rate)) + '%). ' 
      + winner + ' gained the most (' + str(max(change)) + '%) while ' 
      + loser + ', the biggest loser, lost ' + str(min(change)) + '%.')