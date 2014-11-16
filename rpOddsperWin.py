import json, os
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir(".\\rp_json")
path = os.getcwd()
files = ["rp"+str(x)+".json" for x in range(len([name for name in os.listdir('.') if os.path.isfile(name)]))]

x = []
y = []
num_races = 0

for file in files:
  with open(file, "r") as f:
    data = json.loads(f.read())

  for date in data:
    for location in date[2:]:
      for time_race in location[1:]:
        num_races += 1
        for num in range(len(time_race[2])):
          odds = time_race[2][num]
          fav = time_race[1][num]

          if (odds in x) or ((odds.lower() == "evens") and ("1/1" in x)):
            if odds.lower() == "evens":
              index = x.index("1/1")
            else:
              index = x.index(odds)
            y[index] += 1
          else:
            if odds.lower() == "evens":
              x.append("1/1")
            else:
              x.append(odds)
            y.append(1)
x, y = (list(t) for t in zip(*sorted(zip(x, y), key=lambda tup: float(tup[0].split("/")[0])/float(tup[0].split("/")[1]))))

print num_races

fig = plt.figure(figsize=(20, 5))
ax = plt.plot()

index = np.arange(len(x))
x = np.array(x)
y = np.array(y)

graph = plt.plot(index, y)

plt.xlabel("Odds")
plt.ylabel("Num Favs")
plt.xticks(rotation=70)
plt.xticks(np.linspace(0, len(x), len(x)), x)
plt.show()
