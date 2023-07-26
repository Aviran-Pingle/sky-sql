from sqlalchemy import create_engine, text, exc
import queries


class FlightData:
    """
    The FlightData class is a Data Access Layer (DAL) object that provides an
    interface to the flight data in the SQLITE database.
    When the object is created, the class forms connection to the sqlite
    database file, which remains active until the object is destroyed.
    """
    def __init__(self, db_uri: str):
        """
        Initialize a new engine using the given database URI
        """
        self._engine = create_engine(db_uri)

    def _execute_query(self, query: str, params: dict) -> list:
        """
        Execute an SQL query with the params provided in a dictionary,
        and returns a list of records (dictionary-like objects).
        If an exception was raised, print the error, and return an empty list.
        """
        try:
            with self._engine.connect() as connection:
                parameterized_query = text(query)
                res = connection.execute(parameterized_query, params)
                return [dict(zip(res.keys(), row)) for row in res.fetchall()]
        except (exc.SQLAlchemyError, exc.DBAPIError) as e:
            print(e)
            return []

    def get_flight_by_id(self, flight_id: int) -> list:
        """
        Searches for a flight's details using flight ID.
        If the flight was found, returns a list with a single record.
        """
        params = {'id': flight_id}
        return self._execute_query(queries.QUERY_FLIGHT_BY_ID, params)

    def get_flights_by_date(self, day: int, month: int, year: int) -> list:
        """
        Searches for flights details using a given date.
        Returns a list of flights occurred on that date.
        """
        params = {'day': day, 'month': month, 'year': year}
        return self._execute_query(queries.QUERY_FLIGHTS_BY_DATE, params)

    def get_delayed_flights_by_airport(self, airport_code: str) -> list:
        """
        Searches for delayed flights by a given airport code.
        Returns a list of delayed flights on that airport.
        """
        params = {'airport': airport_code}
        return self._execute_query(queries.QUERY_DELAYED_FLIGHTS_BY_AIRPORT,
                                   params)

    def get_delayed_flights_by_airline(self, airline: str) -> list:
        """
        Searches for delayed flights by a given airline.
        Returns a list of delayed flights by that airline.
        """
        params = {'airline': airline}
        return self._execute_query(queries.QUERY_DELAYED_FLIGHTS_BY_AIRLINE,
                                   params)

    def __del__(self):
        """
        Closes the connection to the database when the object is about
        to be destroyed
        """
        self._engine.dispose()
    