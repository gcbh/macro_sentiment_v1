import sys
import io
import json
import datetime
import pytz
import forex_live
from econ_ind import EconomicIndicator
from sentiment_json_encoder import SentimentEncoder
from forex_live import produce_indicators

print(chr(27) + "[2J")

est = pytz.timezone('US/Eastern')
countries = []
for country in sys.argv:
    countries.append(forex_live.country_to_forex_ctry(country))

objects = forex_live.produce_indicators(countries)

print '\nThe Calendar\n'
for ind in objects:
    print '-' * 80
    print ind

for ind in objects:
    if ind.date <= datetime.datetime.today().replace(tzinfo=est):
        print ind
        print 'Our position is: ', ind.position()

##json.dumps(objects[0],cls=SentimentEncoder)


#
#   remember these data services:
#       1. Quandl - much financial data
#       2. Quantopia - minute-level trade price and volume data to 2002
#