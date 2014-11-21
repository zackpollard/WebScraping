# # # #
#
#  For web scraping http://www.racingpost.com/ results
#
#    Info gathered:
#    Date, Location, Time, Did a Favorite Win?, Odds, weather(?)
#
#    Stored using json? csv?
#
# # # #

import sys
import json
import datetime
import re
import operator
import os

import requests
from bs4 import BeautifulSoup as BS
from multiprocessing import Pool

# # # #  To be in loop # # # #
def getData(thread_id, thread_amount, days_wanted, limit_locations, limited_locations, base_url, folder_name):

    url_date = datetime.date.today() - datetime.timedelta(days=((days_wanted/thread_amount)*thread_id) + 1)
    count = 0

    while count < (days_wanted/thread_amount):

        if os.path.isfile(folder_name + os.sep + "rp" + str(url_date) + ".json"):
            url_date = url_date - datetime.timedelta(days=1)
            count += 1
            continue

        print(str(url_date))

        url = base_url + str(url_date)  # makes the url
        main_r = requests.get(url)  # get's the web page
        soup = BS(main_r.text)  # soupify!
        # gets the list of locations
        list_of_Locations = [re.search(b"^([^(]*)", x.string.encode("ascii")).group(0).strip() for x in
                             soup.find("div", {"class": "tabBlock"}).ol.find_all("a")]
        # may get what appears to be the same location twice in a row, this is because I get rid of brackets.
        if not limit_locations:
            limited_locations = list_of_Locations
        date = [str(url_date)]  # creates out first layer of info
        all_times = []
        num_races = 0

        # loops over each course's (location) results
        for table in soup.find("div", {"id": "resultTag"}).find_all("table", {"class": "resultGrid"}):
            if list_of_Locations[0].decode("ISO-8859-1") in limited_locations:
                location = list_of_Locations[0]
                list_of_Locations.pop(0)
                # print(location)
                # loops over each result (time_race)
                for td in table.find_all("td"):
                    try:  # some of the "td" have no info we need so they will fail
                        time_race = [td.strong.get_text(), location.decode("ISO-8859-1")]  # time of race

                        # gets each time's results, needed because sometimes there are two winners
                        results_url = "http://www.racingpost.com/" + td.h4.a["href"]
                        results_r = requests.get(results_url)
                        results_soup = BS(results_r.text)
                        results = []

                        num_races += 1
                        for result in results_soup.find_all("tr"):
                            if result.has_attr("data-hid"):
                                try:
                                    place = int(result.find("h3").string)
                                    # print(result.find("span", {'class': 'black'}).text)
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
                                    pass
                        results_sorted = sorted(results, key=operator.itemgetter(0))
                        time_race.append(results_sorted)
                        all_times.append(time_race)
                    except:
                        pass
        all_times = sorted(all_times, key=operator.itemgetter(0))
        date.append(num_races)
        date = date + all_times

        with open(folder_name + os.sep + "rp" + str(url_date) + ".json", "w") as f:
            f.write(json.dumps(date))

        url_date = url_date - datetime.timedelta(days=1)
        count += 1

def main():

    base_url = "http://www.racingpost.com/horses2/results/home.sd?r_date="
    # url_date = datetime.date(2009, 12, 16)

    folder_name = "rp_allPlaces"
    limit_locations = True
    limited_locations = []
    update = False

    if update:
        files = sorted([name for name in os.listdir('.') if os.path.isfile(name)])
        cwd = os.getcwd()
        os.chdir("." + os.sep + "rp_allPlaces")
        path = os.getcwd()
        last_date = files[-1][2:-5]
        delta = datetime.datetime.strptime(str(datetime.date.today() - datetime.timedelta(days=1)), '%Y-%m-%d') - datetime.datetime.strptime(last_date , '%Y-%m-%d')
        days_wanted = delta.days
        print (last_date)
        if days_wanted == 0:
            print("Nothing to update.")
            sys.exit()
        if days_wanted < 0:
            print("Not sure how you've done that, well done I guess. Or go check your system clock.")
            sys.exit()
        os.chdir(cwd)
    else:
      years_wanted = 10  # number of years of data wanted
      days_wanted = years_wanted * 365

    if limit_locations:
        with open("rpLocationLimit.txt", "r") as f:
            for line in f.read().split("\n"):
                limited_locations.append(line)

    thread_amount = 4

    pool = Pool(processes=thread_amount)

    thread_id = 0

    proc_list = []

    while thread_id < thread_amount:

        proc_list.append(pool.apply_async(getData, args=(thread_id, thread_amount, days_wanted, limit_locations, limited_locations, base_url, folder_name)))
        thread_id += 1

    for i in proc_list:

        i.get()

if __name__ == '__main__':
    main()
