import json, os, operator
from os import listdir
from os.path import isfile, join

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir(".\\rp_jsonRev")
path = os.getcwd()
files = ["rp"+str(x)+".json" for x in range(len([name for name in os.listdir('.') if os.path.isfile(name)]))]

total = []

for file in files:
  with open(file, "r") as f:
    data = json.loads(f.read())

  for date in data:
    write_data = []
    write_data.append(date[0])
    for location in date[2:]:
      for time_race in location[1:]:
        write_data.append([time_race[0]])
        if "F" in time_race[1]:
          write_data[-1].append("F")
        else:
          write_data[-1].append("N")

    sorted_data = [write_data[0]] + sorted(write_data[1:], key=operator.itemgetter(0))
    total.append(sorted_data)

os.chdir("..\\rp_jsonOrdered")
count_name = 0

while len(total) >= 50:
  to_write = total[:50]
  total = total[50:]

  with open("rp" + str(count_name) + ".json", "w") as f:
    f.write(json.dumps(to_write))

  count_name += 1

with open("rp" + str(count_name) + ".json", "w") as f:
  f.write(json.dumps(to_write))
