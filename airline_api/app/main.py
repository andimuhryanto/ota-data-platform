from fastapi import FastAPI, HTTPException
from .flight_generator import FlightGenerator, Dimensions

app = FastAPI()

@app.get("/generateFlights")
def generateFlightsAPI(startDate:str, endDate:str, airlineCode:str, flightType:str, intlFlightDirection=None, numRecords:int=1):
    # Validation Checkings
    isDatesIsStr = isinstance(startDate, str) and isinstance(endDate, str)
    isStartDateBeforeEndDate = int(startDate.replace('-', '')) <= int(endDate.replace('-', ''))
    isAirlineCodeStr = isinstance(airlineCode, str)
    try:
        isNumRecordsInt = isinstance(int(numRecords), int)
    except:
        isNumRecordsInt = False
    isFlightTypeValid = flightType.lower() in ['domestic', 'international']
    isIntlFlightDirectionValid = intlFlightDirection.lower() in ['in', 'out'] if isinstance(intlFlightDirection, str) else intlFlightDirection is None

    paramValid = (
        isDatesIsStr &
        isStartDateBeforeEndDate &
        isAirlineCodeStr &
        isNumRecordsInt &
        isFlightTypeValid &
        isIntlFlightDirectionValid
    )
    try:
        if not paramValid:
            raise HTTPException(status_code=400, detail='Invalid input parameters')
        else:
            FG = FlightGenerator(airlineCode=airlineCode, startDepartureDate=startDate, endDepartureDate=endDate)
            if flightType == 'domestic':
                return FG.generateDomesticFlights(numRecords=numRecords)
            else:
                return FG.generateInternationalFlights(numRecords=numRecords, intlFlightDirection=intlFlightDirection)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
    
@app.get('/airports')
def getAirportsAPI(iataCode:str=None, countryCode:str=None):
    isIATACodeStr = (isinstance(iataCode, str) or iataCode is None)
    isCountryCodeStr = (isinstance(countryCode, str) or countryCode is None)

    paramValid = (isIATACodeStr & isCountryCodeStr)
    try:
        if not paramValid:
            raise HTTPException(status_code=400, detail='Invalid input parameters')
        else:
            dimension = Dimensions()
            return dimension.getAirportList(iataCode=iataCode, countryCode=countryCode)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
    
@app.get('/airlines')
def getAirlinesAPI(airlineCode:str=None, countryCode:str=None):
    isAirlineCodeStr = (isinstance(airlineCode, str) or airlineCode is None)
    isCountryCodeStr = (isinstance(countryCode, str) or countryCode is None)

    paramValid = (isAirlineCodeStr & isCountryCodeStr)
    try:
        if not paramValid:
            raise HTTPException(status_code=400, detail='Invalid input parameters')
        else:
            dimension = Dimensions()
            return dimension.getAirlineList(airlineCode=airlineCode, countryCode=countryCode)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
    
@app.get('/aircraftCarriers')
def getAircraftCarrierLiestAPI(airlineCode:str=None):
    isAirlineCodeStr = (isinstance(airlineCode, str) or airlineCode is None)

    paramValid = (isAirlineCodeStr & True)
    try:
        if not paramValid:
            raise HTTPException(status_code=400, detail='Invalid input parameters')
        else:
            dimension = Dimensions()
            return dimension.getAircraftCarrierLiest(airlineCode=airlineCode)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
            

