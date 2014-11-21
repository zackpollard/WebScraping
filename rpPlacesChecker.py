import json, os, datetime
from os import listdir
from os.path import isfile, join

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir(".\\rp_allPlaces")
path = os.getcwd()
base = datetime.date.today()
files = ["rp"+str(base - datetime.timedelta(days=x))+".json" for x in range(10*365)]

for file in files:
    if os.path.isfile(file):
        with open(file, "r") as f:
            date = json.loads(f.read())
        print("!")
        string_date = date[0]
        no_of_races = date[1]
        if not no_of_races == 0:
            for time_race in date[2:]:
                time_of_race = time_race[0]
                location = time_race[1]
                for result in time_race[2]:
                    place = result[0]
                    fav = result[1]
                    odds = result[2]
        else:
            print("No races in", file)
    else:
        print("Failed on", file)
