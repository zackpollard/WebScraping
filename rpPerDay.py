import json, os, time, datetime, matplotlib
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir(".\\rp_json")
path = os.getcwd()
files = [f for f in listdir(path) if isfile(join(path, f))]

x = []
y = []

for file in files:
  with open(file, "r") as f:
    data = json.loads(f.read())

  for date in data:
    x.append(time.strptime(date[0], '%Y-%m-%d'))
    num_f = 0
    for location in date[1:]:
      for time_race in location[1:]:
        for fav in time_race[1]:
          if fav == "F":
            num_f += 1
    y.append(num_f)

print len(x)
print len(y)

"""plt.scatter(x,y)
plt.gcf().autofmt_xdate()

plt.show()
"""
