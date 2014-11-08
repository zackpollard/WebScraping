####
#
#   For web scraping http://www.racingpost.com/ results
#
#   Info gathered:
#   Date, Location, Time, Did a Favorite Win?, Odds, weather(?)
#
#   Stored using json? csv?
#
####

import json, requests, datetime, re
from bs4 import BeautifulSoup as BS

url_date = datetime.date.today()
url_date = "2014-11-03"

years_wanted = 4
days_wanted = years_wanted*365
base_url = "http://www.racingpost.com/horses2/results/home.sd?r_date="
#today - datetime.timedelta(days = 1)
#^ prev day

#### To be in loop ####
try:
  url = base_url+str(url_date)
  r = requests.get(url)
  soup = BS(r.text)
  info = {}
  list_of_Locations = [re.search("^([^(]*)", x.string.encode("ascii")).group(0).strip() for x in soup.find("div", {"class": "tabBlock"}).ol.find_all("a")]

  for table in soup.find_all("table", {"class": "resultGrid"}):
    for td in table.find_all("td"):
      try:
        time = td.strong.get_text()
        results = td.find_all("p")[1].get_text().strip().encode("ascii").split("\n")
        fav = [] # mostly just one value
        odds = [] # same as above
        for result in results:
          result = result.strip()
          if result[0] == "1":
            try:
              int(result[-1])
              fav.append("N")
              odds.append(result.split()[-1])
            except:
              fav.append(result[-1])
              if "even" in result.split()[-1].lower():
                odds.append("Evens")
              else:
                odds.append(result.split()[-1][:-1])
      except:
        None

except:
  None
