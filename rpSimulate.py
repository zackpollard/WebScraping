import json, os
from os import listdir
from os.path import isfile, join
from numpy import recarray
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir("." + os.sep + "rp_allPlaces")
path = os.getcwd()
files = sorted([name for name in os.listdir('.') if os.path.isfile(name)])

min_num_of_locations = 3
max_num_of_num_of_wins = 5
max_num_of_losses = 10
pounds_to_win = 10.0
bank = 0.0
lowest_bank = 0.0
first_month = None
last_stored_month = None
monthly_totals = []

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
        losses_in_a_row = 0
        wins_today = 0
        running_loss = 0
        for time_race in date[2:]:
            if losses_in_a_row >= max_num_of_losses:
                continue
            if wins_today >= max_num_of_num_of_wins:
                continue
            time_of_race = time_race[0]
            location = time_race[1]

            odds_fav = []
            fav_win = False
            for result in time_race[2]:
                place = result[0]
                fav = result[1]
                odds = result[2]

                if fav == "F":  # get's the favorite's odds
                    if "ev" in odds.lower():
                        odds_fav = [1, 1]
                    elif odds == "Unknown":
                        continue  # anything else?
                    else:
                        odds_fav = odds.split("/")
                    if place == 1:
                        fav_win = True
            if odds_fav == []:
                continue
            need_to_win = pounds_to_win + running_loss
            bet_amount = round((int(odds_fav[1]) * need_to_win) / int(odds_fav[0]), 2)
            print(string_date, time_of_race, bank, odds_fav, fav_win, need_to_win, bet_amount)
            if bank < lowest_bank:
                lowest_bank = bank
            # time.sleep(2)
            bank -= bet_amount
            if fav_win:
                wins_today += 1
                running_loss = 0
                losses_in_a_row = 0
                bank += bet_amount
                bank += round((int(odds_fav[0]) * bet_amount) / int(odds_fav[1]), 2)
            else:
                losses_in_a_row += 1
                running_loss += bet_amount

            bank = round(bank, 2)
    month = string_date.split("-")[1]
    if first_month is None:
        first_month = month
    if last_stored_month is None:
        last_stored_month = month
    elif last_stored_month != month:
        last_stored_month = month
        monthly_totals.append(bank)

    else:
        print(string_date, "does not have enough meetings, skipped.")
print(lowest_bank)
print(monthly_totals)
print(len(monthly_totals))