import sqlalchemy
from sqlalchemy import text

class FlightData:
    def __init__(self, db_uri):
        self.engine = sqlalchemy.create_engine(db_uri)

    def _execute_query(self, query, params=None):
        """
        Executes the given query using the provided parameters and returns the result.
        """
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params)
            return result.mappings().all()

    def get_flight_by_id(self, flight_id):
        """
        Retrieves flight information based on the provided flight ID.
        """
        query = '''
        SELECT flights.id AS ID, origin_airport AS ORIGIN_AIRPORT, destination_airport AS DESTINATION_AIRPORT, airlines.airline AS AIRLINE, departure_delay AS DELAY
        FROM flights
        JOIN airlines ON flights.airline = airlines.id
        WHERE flights.id = :flight_id
        '''
        return self._execute_query(query, {'flight_id': flight_id})

    def get_flights_by_date(self, day, month, year):
        """
        Retrieves flights based on the provided date.
        """
        query = '''
        SELECT flights.id AS ID, origin_airport AS ORIGIN_AIRPORT, destination_airport AS DESTINATION_AIRPORT, airlines.airline AS AIRLINE, departure_delay AS DELAY
        FROM flights
        JOIN airlines ON flights.airline = airlines.id
        WHERE day = :day AND month = :month AND year = :year
        '''
        return self._execute_query(query, {'day': day, 'month': month, 'year': year})

    def get_delayed_flights_by_airline(self, airline_name):
        """
        Retrieves delayed flights based on the provided airline name.
        """
        query = '''
        SELECT flights.id AS ID, origin_airport AS ORIGIN_AIRPORT, destination_airport AS DESTINATION_AIRPORT, airlines.airline AS AIRLINE, departure_delay AS DELAY
        FROM flights
        JOIN airlines ON flights.airline = airlines.id
        WHERE airlines.airline LIKE :airline_name AND departure_delay >= 20
        '''
        return self._execute_query(query, {'airline_name': f'%{airline_name}%'})

    def get_delayed_flights_by_airport(self, airport_code):
        """
        Retrieves delayed flights based on the provided origin airport code.
        """
        query = '''
        SELECT flights.id AS ID, origin_airport AS ORIGIN_AIRPORT, destination_airport AS DESTINATION_AIRPORT, airlines.airline AS AIRLINE, departure_delay AS DELAY
        FROM flights
        JOIN airlines ON flights.airline = airlines.id
        WHERE flights.origin_airport = :airport_code AND departure_delay >= 20
        '''
        return self._execute_query(query, {'airport_code': airport_code})
