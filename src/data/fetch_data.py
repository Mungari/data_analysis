import numpy
import pandas as pd
import json

#import api helper
import importlib.util
spec = importlib.util.spec_from_file_location("module.name", "/home/fmungari/Documents/PythonProg/Data_Analysis/flight_statistics/src/api/flightRadarApi.py")
fr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fr)

#init class instance
api = fr.flightRadar24()

# for airport in api.get_airports()["rows"]:
#     print(airport['icao'])
print(len(api.get_flights()))
