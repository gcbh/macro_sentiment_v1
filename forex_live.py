import urllib2
import datetime
import time
import pytz
from econ_ind import EconomicIndicator
from pytz import all_timezones

def produce_indicators(countries):
    req = urllib2.Request('http://ec.forexprostools.com?ecoDayBackground=%23dedede&defaultFont=%233d3d3d&columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&category=_employment,_economicActivity,_inflation,_credit,_centralBanks,_confidenceIndex,_balance,_Bonds&importance=1,2,3&features=datepicker,timezone,filters&countries=25,32,6,37,72,22,17,39,14,48,10,35,42,7,43,60,45,36,110,11,26,12,46,4,5&calType=week&timeZone=55&lang=1')
    try:
        response = urllib2.urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        page = response.read().split('<')

    gmt = pytz.timezone('Etc/Greenwich')
    est = pytz.timezone('US/Eastern')
    data_objects = []
    date = None
    clock = None
    sentiment = None
    event = None
    actual = None
    forecast = None
    previous = None
    country = None

    for string in page:
        if string.startswith('td'):
            if string.find('first') >= 0:
                if string.split('>')[1] == 'Tentative':
                    clock = 'Tentative'
                else:
                    clock = time.strptime(string.split('>')[1], '%H:%M')
            elif string.find('sentiment') >= 0:
                sentiment = string[string.find('title')+7:string.find('title')+11]
            elif string.find('left event') >= 0:
                event = string.split('>')[1]
            elif string.find('bold act') >= 0:
                actual = string.split('>')[1]
            elif string.find('fore') >= 0:
                forecast = string.split('>')[1]
            elif string.find('prev') >= 0:
                previous = string.split('>')[1]
                print country, event, forecast
                if country in countries and clock != 'Tentative':
                    delta = datetime.timedelta(hours=clock.tm_hour,minutes=clock.tm_min)
                    data = EconomicIndicator((date + delta).astimezone(est), country,sentiment,event,actual,forecast,previous)
                    data_objects.append(data)
            elif string.find('theDay') >= 0:
                date = gmt.localize(datetime.datetime.strptime(string.split('>')[1],'%A, %B %d, %Y'))
        elif string.startswith('span') and string.find('ceFlags') >= 0:
            country = string[string.find('class')+7:]
            country = country[country.find('s')+2:country.index('\"')]
    return data_objects

def country_to_forex_ctry(country):
    if country.upper() == 'US':
        return 'United_States'
    elif country.upper() == 'CA':
        return 'Canada'
    elif country.upper() == 'AUS':
        return 'Australia'
    elif country.upper() == 'CN':
        return 'China'
    elif country.upper() == 'EU':
        return 'Europe'
    elif country.upper() == 'JA':
        return 'Japan'
    elif country.upper() == 'UK':
        return 'United_Kingdom'
    elif country.upper() == 'GE':
        return 'Germany'