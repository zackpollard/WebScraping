import json, os, time, datetime
from os import listdir
from os.path import isfile, join

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir("."+os.sep+"rp_json")
path = os.getcwd()
files = ["rp"+str(x)+".json" for x in range(len([name for name in os.listdir('.') if os.path.isfile(name)]))]

total = []

for file in files:
  with open(file, "r") as f:
    data = json.loads(f.read())

  total += data

total = sorted(total, key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d'))

os.chdir(".."+os.sep+"rp_jsonRev")
count_name = 0

while len(total) >= 50:
  print(len(total))
  to_write = total[:50]
  total = total[50:]

  with open("rp" + str(count_name) + ".json", "w") as f:
    f.write(json.dumps(to_write))

  count_name += 1

print(len(total))
with open("rp" + str(count_name) + ".json", "w") as f:
  f.write(json.dumps(to_write))
