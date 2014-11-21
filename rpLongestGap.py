import json, os, time, datetime, calendar
from os import listdir
from os.path import isfile, join

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir("."+os.sep+"rp_jsonOrdered")
path = os.getcwd()
files = ["rp"+str(x)+".json" for x in range(len([name for name in os.listdir('.') if os.path.isfile(name)]))]

longest_gap = 0
longest_gap_date = ""

for file in files:
  with open(file, "r") as f:
    data = json.loads(f.read())

  for date in data:
    num_race = 0
    gap = -1
    for time_race in date[1:]:
      num_race += 1
      gap += 1
      print_check = False
      if "F" in time_race[1]:
        if longest_gap < gap:
          longest_gap = gap
        if gap == 26:
          longest_gap_date = date[0]
        if gap > 10:
          print(gap, date[0],)
          print_check = True
        gap = -1
      if print_check:
        print(num_race)
print("Longest Gap:", longest_gap, "on", longest_gap_date)
