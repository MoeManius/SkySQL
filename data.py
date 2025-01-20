from sqlalchemy import create_engine, text

# SQL Queries with corrected column names
QUERY_FLIGHT_BY_ID = """
    SELECT flights.ID AS FLIGHT_ID, flights.YEAR, flights.MONTH, flights.DAY, 
           flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT, flights.DEPARTURE_DELAY AS DELAY, 
           airlines.AIRLINE
    FROM flights
    JOIN airlines ON flights.AIRLINE = airlines.ID
    WHERE flights.ID = :id
"""

QUERY_FLIGHTS_BY_DATE = """
    SELECT flights.ID AS FLIGHT_ID, flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT, 
           flights.DEPARTURE_DELAY AS DELAY, airlines.AIRLINE
    FROM flights
    JOIN airlines ON flights.AIRLINE = airlines.ID
    WHERE flights.DAY = :day AND flights.MONTH = :month AND flights.YEAR = :year
"""

QUERY_DELAYED_FLIGHTS_BY_AIRLINE = """
    SELECT flights.ID AS FLIGHT_ID, flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT, 
           flights.DEPARTURE_DELAY AS DELAY, airlines.AIRLINE
    FROM flights
    JOIN airlines ON flights.AIRLINE = airlines.ID
    WHERE airlines.AIRLINE = :airline_name AND flights.DEPARTURE_DELAY >= 20
"""

QUERY_DELAYED_FLIGHTS_BY_AIRPORT = """
    SELECT flights.ID AS FLIGHT_ID, flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT, 
           flights.DEPARTURE_DELAY AS DELAY, airlines.AIRLINE
    FROM flights
    JOIN airlines ON flights.AIRLINE = airlines.ID
    WHERE flights.ORIGIN_AIRPORT = :origin_airport AND flights.DEPARTURE_DELAY >= 20
"""

class FlightData:
    """
    The FlightData class is a Data Access Layer (DAL) object that provides an
    interface to the flight data in the SQLITE database. When the object is created,
    the class forms a connection to the SQLite database file, which remains active
    until the object is destroyed.
    """

    def __init__(self, db_uri):
        """Initialize a new engine using the given database URI."""
        self._engine = create_engine(db_uri)

    def _execute_query(self, query, params):
        """
        Execute an SQL query with the params provided in a dictionary,
        and returns a list of records (dictionary-like objects).
        If an exception was raised, print the error, and return an empty list.
        """
        try:
            with self._engine.connect() as connection:
                result = connection.execute(text(query), params)
                return [row for row in result.mappings()]
        except Exception as e:
            print(f"Error executing query: {e}")
            return []

    def get_flight_by_id(self, flight_id):
        """Search for flight details using flight ID."""
        params = {'id': flight_id}
        return self._execute_query(QUERY_FLIGHT_BY_ID, params)

    def get_flights_by_date(self, day, month, year):
        """Retrieve flights scheduled on a specific date."""
        params = {'day': day, 'month': month, 'year': year}
        return self._execute_query(QUERY_FLIGHTS_BY_DATE, params)

    def get_delayed_flights_by_airline(self, airline_name):
        """Retrieve delayed flights for a specific airline."""
        params = {'airline_name': airline_name}
        return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_AIRLINE, params)

    def get_delayed_flights_by_airport(self, origin_airport):
        """Retrieve delayed flights for a specific origin airport."""
        params = {'origin_airport': origin_airport}
        return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_AIRPORT, params)

    def __del__(self):
        """Close the database connection when the object is destroyed."""
        self._engine.dispose()
