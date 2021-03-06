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

base_url = "http://www.racingpost.com/horses2/results/home.sd?r_date="
url_date = datetime.date.today() - datetime.timedelta(days = 1)
#url_date = datetime.date(2013, 12, 12)

folder_name = "rp_json"
limit_locations = True
limited_locations = []

time_between = 0.5# time between requests in secinds
count = 0
count_name = 0
count_reset = 50

years_wanted = 10#number of years of data wanted
days_wanted = years_wanted*365
#days_wanted = 1
#today - datetime.timedelta(days = 1)
#^ prev day

if limit_locations:
  with open("rpLocationLimit.txt", "r") as f:
    for line in f.read().split("\n"):
      limited_locations.append(line)

data = []
#### To be in loop ####
for i in xrange(days_wanted):
  print str(url_date)

  now = float(time.time())#start time
  url = base_url+str(url_date) #makes the url
  r = requests.get(url) #get's the web page
  soup = BS(r.text) #soupify!
  #gets the list of locations
  list_of_Locations = [re.search("^([^(]*)", x.string.encode("ascii")).group(0).strip() for x in soup.find("div", {"class": "tabBlock"}).ol.find_all("a")]
  #may get what appears to be the same location twice in a row, this is because I get rid of brackets.
  if not limit_locations:
    limited_locations = list_of_Locations
  date = [str(url_date)] #creates out first layer of info
  num_races = 0

  #loops over each course's (location) results
  for table in soup.find("div", {"id": "resultTag"}).find_all("table", {"class": "resultGrid"}):
    if list_of_Locations[0] in limited_locations:
      location = [] #second layer of info
      location.append(list_of_Locations.pop(0))
      #loops over each result (time_race)
      for td in table.find_all("td"):
        try:#some of the "td" have no info we need so they will fail
          time_race = [td.strong.get_text().encode("ascii")] #time of race
          #gets each time's results, needed because sometimes there are two winners
          results = td.find_all("p")[1].get_text().strip().encode("ascii").split("\n")
          fav = [] # mostly just one value
          odds = [] # same as above
          found_first = False
          num_races += 1
          for result in results:
            result = result.strip()#nasty trailing whitespace
            try:
              if result[0] == "1":#gets the winners
                found_first = True
                if result[-1].isupper():
                  fav.append(result[-1])
                  if result.split()[-1][0].isalpha():
                    if ("ev" in result.split()[-1].lower()) or ("odds" in result.split()[-1].lower()):
                      odds.append("Evens")
                    else:
                      odds.append("Unknown")
                  else:
                    odds.append(result.split()[-1][:-1])
                else:
                  fav.append("N")
                  if result.split()[-1][0].isalpha():
                    if ("ev" in result.split()[-1].lower()) or ("odds" in result.split()[-1].lower()):
                      odds.append("Evens")
                    else:
                      odds.append("Unknown")
                  else:
                    odds.append(result.split()[-1])
            except:
              None
          if found_first == False:
            fav.append("N")
            odds.append("Unknown")
          time_race.append(fav)
          time_race.append(odds)
          location.append(time_race)
        except:
          None
      date.append(location)
    else:
      list_of_Locations.pop(0)
  date.insert(1, num_races)
  data.append(date)

  url_date = url_date - datetime.timedelta(days = 1)
  if count > count_reset:
    with open(folder_name + "\\rp"+str(count_name)+".json", "w") as f:
      f.write(json.dumps(data))
      count = -1
      count_name += 1
      data = []
  count += 1

  delay = float(time.time()) - now#how long it took
  if delay < time_between:
    time.sleep(time_between - delay)#so I don't overload the site(or get caught...)

with open(folder_name + "\\rp"+str(count_name)+".json", "w") as f:
  f.write(json.dumps(data))
