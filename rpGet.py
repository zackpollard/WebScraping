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

import sys, json, requests, datetime, time, re
from bs4 import BeautifulSoup as BS

url_date = datetime.date.today()
url_date = "2014-11-03"

time_between = 10.0# time between requests in secinds
years_wanted = 4#number of years of data wanted
days_wanted = years_wanted*365
base_url = "http://www.racingpost.com/horses2/results/home.sd?r_date="
#today - datetime.timedelta(days = 1)
#^ prev day

data = []
count = 0
#### To be in loop ####
for i in range(days_wanted)
  try:
    now = float(time.time())#start time
    url = base_url+str(url_date) #makes the url
    r = requests.get(url) #get's the web page
    soup = BS(r.text) #soupify!
    #gets the list of locations
    list_of_Locations = [re.search("^([^(]*)", x.string.encode("ascii")).group(0).strip() for x in soup.find("div", {"class": "tabBlock"}).ol.find_all("a")]
    date = [str(url_date)] #creates out first layer of info

    #loops over each course's (location) results
    for table in soup.find_all("table", {"class": "resultGrid"}):
      location = [] #second layer of info
      location.append(list_of_Locations.pop(0))
      #loops over each result (time_race)
      for td in table.find_all("td"):
        try:#spme of the "td" have no info we need so they will fail
          time_race = [td.strong.get_text().encode("ascii")] #time of race
          #gets each time's results, needed because sometimes there are two winners
          results = td.find_all("p")[1].get_text().strip().encode("ascii").split("\n")
          fav = [] # mostly just one value
          odds = [] # same as above
          for result in results:
            result = result.strip()#nasty trailing whitespace
            if result[0] == "1":
              if result[-1].isupper():
                fav.append(result[-1])
                if "even" in result.split()[-1].lower():
                  odds.append("Evens")
                else:
                  odds.append(result.split()[-1][:-1])
              else:
                fav.append("N")
                odds.append(result.split()[-1])
          time_race.append(fav)
          time_race.append(odds)
          location.append(time_race)
        except:
          None
      date.append(location)
    data.append(date)
    url_date = url_date - datetime.timedelta(days = 1)
    if count >

    delay = float(time.time()) - now#how long it took
    if delay < time_between:
      time.sleep(time_between - delay)#so I don't overload the site(or get caught...)
  except:
    print "!!!something went wrong!!!"
    sys.exit()
