import json, os
from os import listdir
from os.path import isfile, join

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir("."+os.sep+"rp_allPlaces")
path = os.getcwd()
files = sorted([name for name in os.listdir('.') if os.path.isfile(name)])

for file in files:
  with open(file, "r") as f:
    date = json.loads(f.read())
  string_date = date[0]
  no_of_races = date[1]
  for time_race in date[2:]:
    time_of_race = time_race[0]
    location = time_race[1]
    for result in time_race[2]:
      place = result[0]
      fav = result[1]
      odds = result[2]
