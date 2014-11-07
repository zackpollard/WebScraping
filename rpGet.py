###
#
# For web scraping http://www.racingpost.com/ results
#
# Info gathered:
# Date, Location, Time, Did a Favorite Win?, Odds, weather(?)
#
#Stored using json
#
###

import json, requests, datetime
from bs4 import BeautifulSoup as BS

today = datetime.date.today()
years_wanted = 4
days_wanted = years_wanted*365
