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

for file in files:
  with open(file, "r") as f:
    data = json.loads(f.read())

  for date in data:
    for location in date[2:]:
      for time_race in location[1:]:
        for fav in time_race[1]:
          None
        for odds in time_race[2]:
