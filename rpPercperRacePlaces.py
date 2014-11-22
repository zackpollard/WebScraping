import json, os
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir("." + os.sep + "rp_allPlaces")
path = os.getcwd()
files = sorted([name for name in os.listdir('.') if os.path.isfile(name)])

x = []
y = []
z = []
num_races = 0

for file in files:
    with open(file, "r") as f:
        date = json.loads(f.read())

    string_date = date[0]
    no_of_races = date[1]
    for time_race in date[2:]:
        num_races += 1
        time_of_race = time_race[0]
        location = time_race[1]
        for result in time_race[2]:
            place = result[0]
            fav = result[1]
            odds = result[2]
            if place == 1:
                if odds[1].isalpha():
                    if not odds == "Unknown":
                        if (odds in x) or (("ev" in odds.lower()) and ("1/1" in x)):
                            if "ev" in odds.lower():
                                index = x.index("1/1")
                            y[index] += 1
                            z[index] += 1
                        else:
                            if "ev" in odds.lower():
                                x.append("1/1")
                            y.append(1)
                            z.append(1)
                else:
                    if odds in x:
                        index = x.index(odds)
                        y[index] += 1
                        z[index] += 1
                    else:
                        x.append(odds)
                        y.append(1)
                        z.append(1)
            if odds[1].isalpha():
                if not odds == "Unknown":
                    if (odds in x) or (("ev" in odds.lower()) and ("1/1" in x)):
                        if "ev" in odds.lower():
                            index = x.index("1/1")
                        z[index] += 1
                    else:
                        if "ev" in odds.lower():
                            x.append("1/1")
                        y.append(0)
                        z.append(1)
            else:
                if odds in x:
                    index = x.index(odds)
                    z[index] += 1
                else:
                    x.append(odds)
                    y.append(0)
                    z.append(1)
y = [float(y[i])/float(z[i]) for i in range(len(y))]

x, y = (list(t) for t in zip(*sorted(zip(x, y), key=lambda tup: float(tup[0].split("/")[0])/float(tup[0].split("/")[1]))))


fig = plt.figure(figsize=(20, 7))
ax = plt.plot()

index = np.arange(len(x))
x = np.array(x)
y = np.array(y)

graph = plt.plot(index, y)

plt.xlabel("Odds")
plt.ylabel("Num Wins")
plt.xticks(rotation=90)
plt.xticks(np.linspace(0, len(x), len(x)), x)
plt.show()
