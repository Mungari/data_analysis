import re
from bs4 import BeautifulSoup
from regex import D
import requests
import json
import time

class flightRadar24():
    balanceJsonUrl = 'https://www.flightradar24.com/balance.json' #???
    balanceUrl = None
    baseUrl = 'https://www.flightradar24.com' #Flightradar url
    apiUrl = 'https://api.flightradar24.com/common/v1' #API url
    liveDataUrl = 'https://data-live.flightradar24.com' #Live url

    #Api endpoints dict
    metaDataEndPoints = {
        'airports': '/_json/airports.php', 
        'airlines': '/_json/airlines.php',
        'zones': '/js/zones.js.php'
    }

    #RealTime endpoints dict
    realTimeDataEndPoints = {
        'flight': '/flight/list.json?&fetchBy=flight&page=1&limit=25&query=',  # add flight number e.g: TK1
        'flights': '/zones/fcgi/feed.js?faa=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&estimated=1&gliders=1&stats=1&maxage=14400'
    }

    def __init__(self):
        response = api_request(self.balanceJsonUrl)
        tmp_weight = 0
        tmp_uri = None
        for uri, weight in response.items():
            if weight > tmp_weight:
                tmp_uri = uri
                tmp_weight = weight
        self.balanceUrl = tmp_uri

    def get_airports(self):
        return api_request(self.baseUrl + self.metaDataEndPoints['airports'])

    def get_airlines(self):
        return api_request(self.baseUrl + self.metaDataEndPoints['airlines'])

    def get_flights(self):
        endpoint = self.liveDataUrl + self.realTimeDataEndPoints['flights'] + '&_=' + str(time.time())
        return api_request(endpoint)

    def get_flight(self, flight_id):
        endpoint = self.apiUrl + self.realTimeDataEndPoints['flight'] + flight_id
        return api_request(endpoint)

    def get_zones(self):
        return api_request(self.baseUrl + self.metaDataEndPoints['zones'])

def api_request(end_point):
    request_base_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "accept": "application/json",
    "accept-language": "en-EN",
    "cache-control": "max-age=0",
    "origin": "https://www.flightradar24.com",
    "referer": "https://www.flightradar24.com/"
}
    r = requests.get(end_point, headers=request_base_headers)
    print(end_point)
    if r.status_code == 402:
        raise RuntimeError("Request to " + end_point + " requires payment")
    if r.status_code == 403:
        raise RuntimeError("Request to " + end_point + " is Forbidden")
    if r.status_code == 404:
        raise RuntimeError("Request to " + end_point + " is NotFound")
    if r.status_code == 500:
        raise RuntimeError("Request to " + end_point + " returns InternalServerError")
    return r.json()