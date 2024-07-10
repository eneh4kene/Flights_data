import data
from datetime import datetime
import sqlalchemy
import visualize  # Import the visualize module

SQLITE_URI = 'sqlite:///data/flights.sqlite3'
IATA_LENGTH = 3


def delayed_flights_by_airline(data_manager):
    airline_input = input("Enter airline name: ")
    results = data_manager.get_delayed_flights_by_airline(airline_input)
    print_results(results)


def delayed_flights_by_airport(data_manager):
    valid = False
    while not valid:
        airport_input = input("Enter origin airport IATA code: ")
        if airport_input.isalpha() and len(airport_input) == IATA_LENGTH:
            valid = True
    results = data_manager.get_delayed_flights_by_airport(airport_input)
    print_results(results)


def flight_by_id(data_manager):
    valid = False
    while not valid:
        try:
            id_input = int(input("Enter flight ID: "))
        except Exception as e:
            print("Try again...")
        else:
            valid = True
    results = data_manager.get_flight_by_id(id_input)
    print_results(results)


def flights_by_date(data_manager):
    valid = False
    while not valid:
        try:
            date_input = input("Enter date in DD/MM/YYYY format: ")
            date = datetime.strptime(date_input, '%d/%m/%Y')
        except ValueError as e:
            print("Try again...", e)
        else:
            valid = True
    results = data_manager.get_flights_by_date(date.day, date.month, date.year)
    print_results(results)


def print_results(results):
    print(f"Got {len(results)} results.")
    for result in results:
        try:
            delay = int(result['DELAY']) if result['DELAY'] else 0
            origin = result['ORIGIN_AIRPORT']
            dest = result['DESTINATION_AIRPORT']
            airline = result['AIRLINE']
        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results: ", e)
            return

        if delay and delay > 0:
            print(f"{result['ID']}. {origin} -> {dest} by {airline}, Delay: {delay} Minutes")
        else:
            print(f"{result['ID']}. {origin} -> {dest} by {airline}")


def show_menu_and_get_input():
    print("Menu:")
    for key, value in FUNCTIONS.items():
        print(f"{key}. {value[1]}")

    while True:
        try:
            choice = int(input())
            if choice in FUNCTIONS:
                func, needs_data_manager = FUNCTIONS[choice][0], FUNCTIONS[choice][2]
                return func, needs_data_manager
        except ValueError as e:
            pass
        print("Try again...")


FUNCTIONS = {
    1: (flight_by_id, "Show flight by ID", True),
    2: (flights_by_date, "Show flights by date", True),
    3: (delayed_flights_by_airline, "Delayed flights by airline", True),
    4: (delayed_flights_by_airport, "Delayed flights by origin airport", True),
    5: (visualize.percentage_delayed_flights_per_airline, "Visualize percentage of delayed flights per airline", False),  # No data_manager needed
    6: (quit, "Exit", False)
}


def main():
    data_manager = data.FlightData(SQLITE_URI)
    while True:
        choice_func, needs_data_manager = show_menu_and_get_input()
        if needs_data_manager:
            choice_func(data_manager)
        else:
            choice_func()


if __name__ == "__main__":
    main()
