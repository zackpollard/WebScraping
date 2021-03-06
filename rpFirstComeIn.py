############
#
#
# Added some date stuff to the labels, not fulle working probably
#
#
############
import json, os, time, datetime, matplotlib, calendar
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir("."+os.sep+"rp_jsonOrdered")
path = os.getcwd()
files = ["rp"+str(x)+".json" for x in range(len([name for name in os.listdir('.') if os.path.isfile(name)]))]

x = []#list of dates
y = []#list of data
years = []#for the labels
#v- for the average line
count = -1
avg = []
avg_last = 365
first_date = True
date_check = ""

for file in files:
  with open(file, "r") as f:
    data = json.loads(f.read())

  for date in data:
    count += 1
    x.append(time.strptime(date[0], '%Y-%m-%d'))
    if first_date:
      date_check = date[0][5:]
      first_date = False
      print(date_check)
    if date[0][5:] == date_check:
      years.append(calendar.month_name[int(date[0][5:7])][:3] + " " + date[0][:4])
    num_race = 0
    for time_race in date[1:]:
      num_race += 1
      if "F" in time_race[1]:
        break

    if num_race > 10:
      print(date[0])

    y.append(num_race)
    if count == avg_last:
      l = y[-avg_last:]
      avg.append(sum(l) / float(len(l)))
      count = -1

ax = plt.figure(figsize=(30,10))

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
