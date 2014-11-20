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

import sys, json, requests, datetime, time, re, operator, os
from bs4 import BeautifulSoup as BS

base_url = "http://www.racingpost.com/horses2/results/home.sd?r_date="
url_date = datetime.date.today() - datetime.timedelta(days = 1)
url_date = datetime.date(2009, 12, 12)

folder_name = "rp_allPlaces"
limit_locations = True
limited_locations = []
update = False

time_between = 0.5# time between requests in secinds
if update:
  cwd = os.getcwd()
  os.chdir(".\\" + folder_name)
  count_name = len([name for name in os.listdir('.') if os.path.isfile(name)])
  os.chdir(cwd)
else:
  count_name = 0

years_wanted = 10#number of years of data wanted
days_wanted = years_wanted*365
days_wanted = 10
#today - datetime.timedelta(days = 1)
#^ prev day

if limit_locations:
  with open("rpLocationLimit.txt", "r") as f:
    for line in f.read().split("\n"):
      limited_locations.append(line)

#### To be in loop ####
for i in xrange(days_wanted):
  print str(url_date)

  now = float(time.time())#start time
  url = base_url+str(url_date) #makes the url
  main_r = requests.get(url) #get's the web page
  soup = BS(main_r.text) #soupify!
  #gets the list of locations
  list_of_Locations = [re.search("^([^(]*)", x.string.encode("ascii")).group(0).strip() for x in soup.find("div", {"class": "tabBlock"}).ol.find_all("a")]
  #may get what appears to be the same location twice in a row, this is because I get rid of brackets.
  if not limit_locations:
    limited_locations = list_of_Locations
  date = [str(url_date)] #creates out first layer of info
  all_times = []
  num_races = 0

  #loops over each course's (location) results
  for table in soup.find("div", {"id": "resultTag"}).find_all("table", {"class": "resultGrid"}):
    if list_of_Locations[0] in limited_locations:
      location = list_of_Locations[0]
      list_of_Locations.pop(0)
      #print location
      #loops over each result (time_race)
      for td in table.find_all("td"):
        try:#some of the "td" have no info we need so they will fail
          time_race = [td.strong.get_text().encode("ascii"), location] #time of race
          #gets each time's results, needed because sometimes there are two winners
          results_url = "http://www.racingpost.com/" + td.h4.a["href"]
          results_r = requests.get(results_url)
          results_soup = BS(results_r.text)
          results = []

          num_races += 1
          for result in results_soup.find_all("tr"):
            if result.has_attr("data-hid"):
              try:
                place = int(result.find("h3").string)
                #print result.find("span", {'class': 'black'}).text
                odds_fav = result.find("span", {'class': 'black'}).text.split(" ")[-2]
                if odds_fav[-1].isupper():
                  fav = odds_fav[-1]
                  if odds_fav[0].isalpha():
                    if "ev" in odds_fav[-1].lower() or "odds" in odds_fav[-1].lower():
                      odds = "Evens"
                    else:
                      odds = "Unknown"
                  else:
                    odds = odds_fav[:-1]
                else:
                  fav = "N"
                  if odds_fav[0].isalpha():
                    if "ev" in odds_fav[-1].lower() or "odds" in odds_fav[-1].lower():
                      odds = "Evens"
                    else:
                      odds = "Unknown"
                  else:
                    odds = odds_fav
                results.append([place, fav, odds])
              except:
                None
          results_sorted = sorted(results, key=operator.itemgetter(0))
          time_race.append(results_sorted)
          all_times.append(time_race)
        except:
          None
  all_times = sorted(all_times, key=operator.itemgetter(0))
  date.append(num_races)
  date = date + all_times

  with open(folder_name+"\\rp"+str(count_name)+".json", "w") as f:
    f.write(json.dumps(date))
    count_name += 1

  url_date = url_date - datetime.timedelta(days = 1)
