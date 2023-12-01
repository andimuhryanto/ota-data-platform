import random
from datetime import datetime, timedelta

import os

from .ota_utils import *

class FlightGenerator:
    def __init__(self, airlineCode:str, startDepartureDate:str=None, endDepartureDate:str=None, USDRate=0.12):
        self.fileDir = 'app/dimensions' if os.getcwd() == '/code' else 'dimensions'
        self._getAirlineDetails(airlineCode)
        self.startDepartureDate = startDepartureDate if startDepartureDate is None else parseDate(startDepartureDate)
        self.endDepartureDate = endDepartureDate if endDepartureDate is None else parseDate(endDepartureDate)
        self.USDRate = USDRate
        self._getAirports()

    def _getAirlineDetails(self, airlineCode):
        self.airlineCode = airlineCode
        self.airline = filterList(readCsv(self.fileDir + '/airlines.csv'), {'code': ('==', self.airlineCode)})
        self.airline = filterList(readCsv(self.fileDir + '/airlines.csv'), {'code': ('==', self.airlineCode)})[0]
        self.airlineId = self.airline['id']
        self.airlineCountryCode = self.airline['countryCode']
        self.aircraftCarriers = filterList(readCsv(self.fileDir + '/aircraft_carriers.csv'), {'airlineId': ('==', self.airlineId)})
        self.aircraftCarriersActive = filterList(self.aircraftCarriers, {'aircraftStatus': ('==', 'ACTIVE')})

    def _getAirports(self):
        self.airportsLocal = filterList(readCsv(self.fileDir + '/airports.csv'), {'countryCode': ('==', self.airlineCountryCode)})
        self.airportsForeign = filterList(readCsv(self.fileDir + '/airports.csv'),{'countryCode': ('!=', self.airlineCountryCode)})

    def _setAirlineCode(self, airlineCode:str):
        self._getAirlineDetails(airlineCode)

    def setFareRate(self, USDRate):
        self.fareRate = USDRate

    def setDepartureDateRange(self, startDate, endDate):
        self.startDepartureDate = self._parseDate(startDate)
        self.endDepartureDate = self._parseDate(endDate)

    def setStartDepartureDates(self, startDate):
        self.startDepartureDate = self._parseDate(startDate)

    def setEndDepartureDates(self, endDate):
        self.endDepartureDate = self._parseDate(endDate)
    
    def _calculateFare(self, distance):
        return self.USDRate * distance
    
    def _sampleAirport(self, domestic=True):
        if domestic:
            return random.choice(self.airportsLocal)
        else:
            return random.choice(self.airportsForeign)
    def _sampleAircraftCarrier(self):
        return random.choice(self.aircraftCarriersActive)
    
    def _generateFlight(self, startDate, endDate, domestic=True, intlFlightDirection=None):
        
        aircraftCarrier = self._sampleAircraftCarrier()
        domesticAirport = self._sampleAirport()
        counterAirport = self._sampleAirport() if domestic else self._sampleAirport(domestic=False)

        distanceKm = calculateDistance(
            originCoord=(domesticAirport['lat'], domesticAirport['lon']), 
            destinationCoord=(counterAirport['lat'], counterAirport['lon'])
        )

        fare = self._calculateFare(distanceKm)
        departureTime = randomDate(startDate, endDate, includeTime=True)
        
        if intlFlightDirection == 'in': # To Domestic Airport 
            originAirport, destinationAirport = counterAirport, domesticAirport
        elif intlFlightDirection == 'out': # From Domestic Airport 
            originAirport, destinationAirport = domesticAirport, counterAirport
        else: # Random Direction
            originAirport, destinationAirport = random.choices([domesticAirport, counterAirport], k=2)

        flight = {
            'airline': self.airline
            , 'aircraftCarrier': aircraftCarrier
            , 'origin': originAirport
            , 'destination': destinationAirport
            , 'departureTime': departureTime.strftime('%Y-%m-%d %H:%M:%S')
            , 'distanceKm': distanceKm
            , 'fareUSD': fare
        }

        return flight

    def generateDomesticFlights(self, numRecords:int=1):
        flights = [self._generateFlight(self.startDepartureDate, self.endDepartureDate) for _ in range(numRecords)]
        return flights
    
    def generateInternationalFlights(self, numRecords:1, intlFlightDirection=None):
        flights = []
        for _ in range(numRecords):
            flight = self._generateFlight(self.startDepartureDate, self.endDepartureDate, domestic=False, intlFlightDirection=intlFlightDirection)
            flights.append(flight)

        return flights

class Dimensions:
    def __init__(self):
        self.fileDir = 'app/dimensions' if os.getcwd() == '/code' else 'dimensions'
        
    def getAirportList(self, countryCode=None, iataCode=None):
        filters = {}
        airports = readCsv(self.fileDir + '/airports.csv')

        if countryCode: filters.update({'countryCode': ('==', countryCode)})
        if iataCode: filters.update({'iata': ('==', iataCode)})

        if filters:
            airports = filterList(airports, conditions=filters)
        
        return airports

    def getAirlineList(self, airlineCode=None, countryCode=None):
        filters = {}
        airlines = readCsv(self.fileDir + '/airlines.csv')
        if countryCode: filters.update({'countryCode': ('==', countryCode)})
        if airlineCode: filters.update({'code': ('==', airlineCode)})

        if filters:
            airlines = filterList(airlines, conditions=filters)
        
        return airlines
    
    def getAircraftCarrierLiest(self, airlineCode=None):
        filters = {}
        aircraftCarriers = readCsv(self.fileDir + '/aircraft_carriers.csv')

        if airlineCode: filters.update({'airlineCode': ('==', airlineCode)})
        if filters:
            aircraftCarriers = filterList(aircraftCarriers, conditions=filters)
        
        return aircraftCarriers


#FG = FlightGenerator(airlineCode='GA', startDepartureDate='2023-01-01', endDepartureDate='2023-01-02')
#print(FG.airline)
#print(FG.airportsLocal[0]['countryCode'], FG.airportsForeign[0]['countryCode'])
#print(FG.startDepartureDate, FG.endDepartureDate)
#print(FG.generateDomesticFlights(1))
#print(FG.generateInternationalFlights(1, intlFlightDirection='out'))
#print([airport['name'] for airport in FG.getAirportList(countryCode='IDN', iataCode='CGK')])
#print(FG.getAirlineList(countryCode='IDN'))
#print(FG.getAircraftCarrierLiest(airlineCode='GA'))