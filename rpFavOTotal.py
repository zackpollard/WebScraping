import json, os, time, datetime, matplotlib
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir("."+ os.sep+"rp_jsonRev")
path = os.getcwd()
files = ["rp"+str(x)+".json" for x in range(len([name for name in os.listdir('.') if os.path.isfile(name)]))]

x = []
y = []
years = []
count = -1
avg = []
avg_last = 365

for file in files:
  with open(file, "r") as f:
    data = json.loads(f.read())

  for date in data:
    if not date[0][:4] in years:
      years.append(date[0][:4])
    num_f = 0.0
    total_f = 0.0
    for location in date[2:]:
      for time_race in location[1:]:
        for fav in time_race[1]:
          if fav == "F":
            num_f += 1
          total_f += 1
    if num_f == 0:
      print(date[0])
    if date[0] == "2011-12-24":
      print(date[1:])
    if total_f != 0:
      if num_f/total_f == 1:
        print(">" + date[0])
      count += 1
      x.append(time.strptime(date[0], '%Y-%m-%d'))
      y.append(num_f/total_f)
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

graph = plt.plot(index, y, 'o', color="blue")
graph2 = plt.plot(index2, avg, color="red")

plt.xlabel("Date")
plt.ylabel("No. of Favs/Total Races")
plt.xticks(np.linspace(0, len(y), len(years)), years)
plt.title("Number of favorites to come in per day")
plt.show()
