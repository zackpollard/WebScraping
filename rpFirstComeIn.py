#######
#
#
# Need to order the dates
#
#
#######
import json, os, time, datetime, matplotlib
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir(".\\rp_jsonRev")
path = os.getcwd()
files = ["rp"+str(x)+".json" for x in range(len([name for name in os.listdir('.') if os.path.isfile(name)]))]

x = []#list of dates
y = []#list of data
years = []#for the labels
#v- for the average line
count = -1
avg = []
avg_last = 365

for file in files:
  with open(file, "r") as f:
    data = json.loads(f.read())

  for date in data:
    count += 1
    x.append(time.strptime(date[0], '%Y-%m-%d'))
    if not date[0][:4] in years:
      years.append(date[0][:4])
    num_race = 0
    for location in date[2:]:
      for time_race in location[1:]:
        num_race += 1
        for fav in time_race[1]:
          if fav == "F":
            break;

    y.append(num_race)
    if count == avg_last:
      l = y[-avg_last:]
      avg.append(sum(l) / float(len(l)))
      count = -1

ax = plt.figure(figsize=(30,5))

index = np.arange(len(x))
index2 = np.linspace(0, len(x), len(avg))
y = np.array(y)
x = np.array(x)
avg = np.array(avg)

graph = plt.plot(index, y, color="blue")
graph2 = plt.plot(index2, avg, color="red")

plt.xlabel("Time")
plt.ylabel("What race the first Fav come in on.")
plt.xticks(np.linspace(0, len(y), len(years)), years)
plt.title("When did the first favorite come in on ")
plt.show()
