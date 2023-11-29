import random
import csv
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
import os

class FlightGenerator:
    def __init__(self, airlineCode=None, startDepartureDate=None, endDepartureDate=None, n=1, USDperKMRate=0.12):
        self.airlineCode = airlineCode
        self.startDepartureDate = startDepartureDate
        self.endDepartureDate = endDepartureDate
        self.n = n
        self.fareRate = USDperKMRate

        fileDir = 'app/dimensions' if os.getcwd() == '/code' else 'dimensions'
        airlines = self._readCsv(fileDir + '/airlines.csv', delimiter='|')
        self.airlines = airlines
        self.aircraftCarriers = self._readCsv(fileDir + '/aircraft_carriers.csv', delimiter='|')
        self.airports = self._readCsv(fileDir + '/airports.csv', delimiter='|')
        self.airline = None

        if airlineCode is not None:
            self.airline = self._getAirline(airlineCode)

    @staticmethod
    def _readCsv(filePath, delimiter=','):
        with open(filePath, 'r') as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            return list(reader)

    @staticmethod
    def _parseDate(dateStr):
        try:
            return datetime.strptime(dateStr, '%Y-%m-%d')
        except ValueError:
            return datetime.strptime(dateStr, '%Y%m%d')

    @staticmethod
    def _randomDate(startDate, endDate):
        return startDate + timedelta(
            days=random.randint(0, (endDate - startDate).days)
        )

    def setFareRate(self, usd_km_rate):
        self.fareRate = usd_km_rate

    def setAirlineCode(self, airlineCode):
        self.airlineCode = airlineCode
        self.airline = self._getAirline(airlineCode)

    def setDepartureDates(self, startDate, endDate):
        self.startDepartureDate = self._parseDate(startDate)
        self.endDepartureDate = self._parseDate(endDate)

    def setStartDepartureDates(self, startDate):
        self.startDepartureDate = self._parseDate(startDate)

    def setEndDepartureDates(self, endDate):
        self.endDepartureDate = self._parseDate(endDate)

    def setNRecords(self, n):
        try:
            self.nRecords = n
        except:
            self.nRecords = int(n)

    def _getAirline(self, airlineCode):
        for airline in self.airlines:
            if airline['code'] == airlineCode:
                return airline

    def _getAirlineCountry(self):
        return self.airline['countryCode']

    def _getAirport(self, countryCode, domestic=True):
        if domestic:
            airportsInCountry = [airport for airport in self.airports if airport['countryCode'] == countryCode]
            return random.choice(airportsInCountry)
        else:
            foreignAirports = [airport for airport in self.airports if airport['countryCode'] != countryCode]
            return random.choice(foreignAirports)

    def _calculateDistance(self, origin_coord, destination_coord):
        # Haversine Formula
        lat1, lon1 = [float(v) for v in origin_coord]
        lat2, lon2 = [float(v) for v in destination_coord]

        # Radius of the Earth in kilometers
        R = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Calculate the differences between latitudes and longitudes
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Haversine formula
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Calculate the distance
        distance = R * c

        return distance

    def _calculateFare(self, distance):
        return self.fareRate * distance

    def _generateFlight(self, startDate, endDate, domestic=True, domesticAirport=None, inCountryFlight=True, returnDetails=True):
        airlineCountry = self._getAirlineCountry()
        airport1 = self._getAirport(airlineCountry, domestic=domestic)

        if domestic:
            airport2 = self._getAirport(airlineCountry, domestic=domestic)
        else:
            destinationCountry = airlineCountry if inCountryFlight else random.choice(
                [airport['countryCode'] for airport in self.airports if airport['countryCode'] != airlineCountry])
            airport2 = self._getAirport(destinationCountry, domestic=not domestic)

        airportPairs = [airport1, airport2]

        if domesticAirport is None:
            random.shuffle(airportPairs)
        else:
            if domesticAirport == 0:
                airportPairs = [airport1, airport2]
            else:
                airportPairs = [airport2, airport1]
        departureAirport, destinationAirport = airportPairs
        distanceKm = self._calculateDistance(
            [departureAirport['lat'], departureAirport['lon']], [destinationAirport['lat'], destinationAirport['lon']])
        fare = self._calculateFare(distanceKm)

        airlineValues = self.airline if returnDetails else {'code': self.airline['code']}
        departureAirportValues = departureAirport if returnDetails else {'iata': departureAirport['iata']}
        destinationAirportValues = destinationAirport if returnDetails else {'iata': destinationAirport['iata']}

        flight = {
            'airline': airlineValues,
            'departureAirport': departureAirportValues,
            'destinationAirport': destinationAirportValues,
            'departureDate': self._randomDate(startDate, endDate).strftime('%Y-%m-%d'),
            'distanceKm': distanceKm,
            'fare_usd': fare
        }
        return flight

    def generateDomesticFlights(self, startDate=None, endDate=None, n=None, returnDetails=True):
        startDate = self.startDepartureDate if startDate is None else self._parseDate(startDate)
        endDate = self.endDepartureDate if endDate is None else self._parseDate(endDate)
        n = self.nRecords if n is None else n

        domesticFlights = []
        for _ in range(n):
            flight = self._generateFlight(startDate, endDate, domestic=True, returnDetails=returnDetails)
            domesticFlights.append(flight)

        return domesticFlights

    def generateInternationalFlights(self, startDate=None, endDate=None, n=None, domesticDeparture=None, inCountryFlight=True, returnDetails=True):
        startDate = self.startDepartureDate if startDate is None else self._parseDate(startDate)
        endDate = self.endDepartureDate if endDate is None else self._parseDate(endDate)
        n = self.nRecords if n is None else n

        internationalFlights = []
        for _ in range(n):
            flight = self._generateFlight(startDate, endDate, domestic=False, domesticAirport=domesticDeparture,
                                          inCountryFlight=inCountryFlight, returnDetails=returnDetails)
            internationalFlights.append(flight)

        return internationalFlights
