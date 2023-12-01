import csv
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
import random

def readCsv(filePath, delimiter='|'):
     with open(filePath, 'r') as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            return list(reader)
     
def filterList(data, conditions):
    filtered_list = []
    for d in data:
        if all(
            (condition == "==" and d.get(key) == value) or
            (condition == "!=" and d.get(key) != value) or
            (condition == "<" and d.get(key) < value) or
            (condition == ">" and d.get(key) > value) or
            (condition == "<=" and d.get(key) <= value) or
            (condition == ">=" and d.get(key) >= value)
            for key, (condition, value) in conditions.items()
        ):
            filtered_list.append(d)
    return filtered_list

def parseDate(dateStr):
        try:
            return datetime.strptime(dateStr, '%Y-%m-%d')
        except ValueError:
            return datetime.strptime(dateStr, '%Y%m%d')

def randomDate(startDate, endDate, includeTime=False):
        randomDate = startDate + timedelta(
            days=random.randint(0, (endDate - startDate).days)
        ) 
        if includeTime:
             randomDate += timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
             
        return randomDate

def calculateDistance(originCoord, destinationCoord):
    lat1, lon1 = [float(v) for v in originCoord]
    lat2, lon2 = [float(v) for v in destinationCoord]

    R = 6371.0 # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance