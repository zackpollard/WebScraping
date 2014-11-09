import json, os
from os import listdir
from os.path import isfile, join

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir(".\\rp_json")
path = os.getcwd()
files = [f for f in listdir(path) if isfile(join(path, f))]

for file in files:
  with open(file, "r") as f:
    data = json.loads(f.read())

  for date in data:
    for location in date[1:]:
      for time_race in location[1:]:
        for fav in time_race[1]:
          
