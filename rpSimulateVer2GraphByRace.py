import json, os, time
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir("."+os.sep+"rp_allPlaces")
path = os.getcwd()
files = sorted([name for name in os.listdir('.') if os.path.isfile(name)])

min_num_of_locations = 3
max_num_of_losses = 50
median_odd = 4/1
spread = 1
pounds_to_win = 10
bank = 0.0
lowest_bank = 0.0

x = []  # time
y = []  # bank

losses_in_a_row = 0
running_loss = 0
odds_win = []
win = False
last_total = 0
last_bank = 0

for file in files:
    with open(file, "r") as f:
        date = json.loads(f.read())

    string_date = date[0]
    no_of_races = date[1]
    locations = []
    for time_race in date[2:]:
        if not time_race[1] in locations:
            locations.append(time_race[1])

    """exclusions = ["2004", "2005"]  # might not work??
    for exclusion in exclusions:
        if exclusion in string_date:
            continue"""

    if len(locations) >= min_num_of_locations:
        for time_race in date[2:]:
            if losses_in_a_row >= max_num_of_losses:
                running_loss = 0
                losses_in_a_row = 0
            time_of_race = time_race[0]
            location = time_race[1]
            last_total = 0

            for result in time_race[2]:
                place = result[0]
                fav = result[1]
                odds = result[2]


                if odds[1].isalpha():
                    if "ev" in odds.lower():
                        odds = [1, 1]
                    else:
                        continue  # anything else?
                else:
                    odds = odds.split("/")

                total_odds = int(odds[0]) / int(odds[1])
                if (total_odds < median_odd+spread and total_odds > median_odd-spread) and (abs(median_odd-total_odds) < abs(median_odd-last_total)):
                    last_total = total_odds
                    odds_win = odds

                    if place == 1:
                        win = True
                    else:
                        win = False
            if odds_win == []:
                continue
                #print(string_date)
            #total_odds = int(odds_win[0]) / int(odds_win[1])
            need_to_win = pounds_to_win + running_loss
            bet_amount = round((int(odds_win[1])*need_to_win)/int(odds_win[0]), 2)
            #print(string_date, time_of_race, bank, odds_win, win, need_to_win, bet_amount)
            if bank < lowest_bank:
                lowest_bank = bank
            bank -= bet_amount
            if win:
                running_loss = 0
                losses_in_a_row = 0
                bank += bet_amount
                bank += round((int(odds_win[0])*bet_amount)/int(odds_win[1]), 2)
            else:
                losses_in_a_row += 1
                running_loss += bet_amount

            bank = round(bank, 2)
            x.append(1)
            y.append(bank)
            #print(bank, bet_amount, odds_win)
            #time.sleep(0.01)
            if last_bank == bank:
                print(string_date)
            last_bank = bank

    else:
        pass
        #print(string_date, "does not have enough meetings, skipped.")
print(lowest_bank)

ax = plt.figure(figsize=(30,10))

index = np.arange(len(x))
y = np.array(y)
x = np.array(x)

graph = plt.plot(index, y)

plt.xlabel("Time")
plt.ylabel("The bank")
plt.show()
os.chdir("..")
#plt.savefig("WeInDaMonnies.png")
