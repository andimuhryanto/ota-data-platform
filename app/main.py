from fastapi import FastAPI, HTTPException, Query
from .flight_generator import FlightGenerator

app = FastAPI()

flight_generator = FlightGenerator()

@app.get("/generate_flights")
def generate_flights(startDate: str, endDate: str, n: int, airlineCode: str, flightType: str = "both", returnDetails: bool = True, inCountryFlight: bool = True):
    try:
        if not startDate or not endDate or n <= 0 or not airlineCode:
            raise HTTPException(status_code=400, detail="Invalid input parameters")
        
        flight_generator.setAirlineCode(airlineCode)
        flight_generator.setDepartureDates(startDate, endDate)
        flight_generator.setNRecords(n)

        if flightType.lower() == "domestic":
            domestic_flights = flight_generator.generateDomesticFlights(returnDetails=returnDetails)
            return {"domestic_flights": domestic_flights}
        elif flightType.lower() == "international":
            international_flights = flight_generator.generateInternationalFlights(
                returnDetails=returnDetails, inCountryFlight=inCountryFlight
            )
            return {"international_flights": international_flights}
        else:
            domestic_flights = flight_generator.generateDomesticFlights(returnDetails=returnDetails)
            international_flights = flight_generator.generateInternationalFlights(
                returnDetails=returnDetails, inCountryFlight=inCountryFlight
            )
            return {"domestic_flights": domestic_flights, "international_flights": international_flights}
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
