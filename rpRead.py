import json, os
from os import listdir
from os.path import isfile, join

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir(".\\rp_json")
path = os.getcwd()
files = [f for f in listdir(path) if isfile(join(path, f))]

for file in files:
  with open(file, "r") as f:
    test = json.loads(f.read())


  for date in test:
    print date[0]
    for location in date[1:]:
      print "  " + location[0]
      for time in location[1:]:
        print "    " + time[0]
        for info in time[1:]:
          print "      " + ", ".join(info)
