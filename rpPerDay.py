import json, os, time, datetime, matplotlib
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir(".\\rp_jsonRev")
path = os.getcwd()
files = ["rp"+str(x)+".json" for x in range(len([name for name in os.listdir('.') if os.path.isfile(name)]))]

x = []
y = []
years = []

for file in files:
  with open(file, "r") as f:
    data = json.loads(f.read())

  for date in data:
    x.append(time.strptime(date[0], '%Y-%m-%d'))
    if not date[0][:4] in years:
      years.append(date[0][:4])
    num_f = 0
    for location in date[1:]:
      for time_race in location[1:]:
        for fav in time_race[1]:
          if fav == "F":
            num_f += 1
    if num_f == 0:
      print date[0]
    y.append(num_f)

ax = plt.figure(figsize=(30,5))

index = np.arange(len(x))
bar_width = 1

rects = plt.bar(index, y, bar_width, color="b")


plt.xlabel("Time")
plt.ylabel("No. Per day")
plt.xticks(np.linspace(0, len(y), len(years)), years)
plt.title("Number of favorites to come in per day")
plt.show()
