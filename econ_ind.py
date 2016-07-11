import math
from json import JSONEncoder
from encodable_object import EncodableObject

class EconomicIndicator(EncodableObject):
    def __init__(self, date, country, sentiment, event, actual, forecast, prev_actual):
        EncodableObject.__init__(self)
        self.date = date
        self.country = country
        self.sentiment = sentiment
        self.event = event
        self.actual = actual
        self.forecast = forecast
        self.prev_actual = prev_actual

    def __str__(self):
        return '{date} {country} | {event} Actual: {actual}  Forecast: {forecast}'.format(date = self.date.strftime('%Y-%m-%d %H:%M'), country = self.country, event = self.event, actual = self.actual, forecast = self.forecast)

    __refr__ = __str__

    def position(self):
        if self.actual == '&nbsp;':
            return None

        fore = None
        act = None
        
        if self.forecast.find('%') >= 0:
            fore = self.forecast.split('%')[0]
            act = self.actual.split('%')[0]
        elif self.forecast.find('B') >= 0:
            fore = self.forecast.split('B')[0]
            act = self.actual.split('B')[0]
        elif self.forecast.find('T') >= 0:
            fore = self.forecast.split('T')[0]
            act = self.actual.split('T')[0]
        else:
            fore = self.forecast
            act = self.actual

        return (float(act) - float(fore)) / math.fabs(float(act))