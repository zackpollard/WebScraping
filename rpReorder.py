import json, os, time, operator
from os import listdir
from os.path import isfile, join

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir(".\\rp_json")
path = os.getcwd()
files = ["rp"+str(x)+".json" for x in range(len([name for name in os.listdir('.') if os.path.isfile(name)]))]

total = []

for file in files:
  with open(file, "r") as f:
    data = json.loads(f.read())

  total += data

total = sorted(total, key=operator.itemgetter(0))

os.chdir("..\\rp_jsonRev")
count_name = 0

while len(total) > 50:
  to_write = total[:50]
  total = total[50:]

  with open("rp" + str(count_name) + ".json", "w") as f:
    f.write(json.dumps(to_write))

  count_name += 1

with open("rp" + str(count_name) + ".json", "w") as f:
  f.write(json.dumps(to_write))
