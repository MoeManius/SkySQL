import data
from datetime import datetime
import sqlalchemy

SQLITE_URI = 'sqlite:///data/flights.sqlite3'
IATA_LENGTH = 3


def delayed_flights_by_airline(data_manager):
    airline_input = input("Enter airline name: ")
    results = data_manager.get_delayed_flights_by_airline(airline_input)
    print_results(results)


def delayed_flights_by_airport(data_manager):
    while True:
        airport_input = input("Enter origin airport IATA code: ")
        if airport_input.isalpha() and len(airport_input) == IATA_LENGTH:
            break
    results = data_manager.get_delayed_flights_by_airport(airport_input)
    print_results(results)


def flight_by_id(data_manager):
    while True:
        try:
            id_input = int(input("Enter flight ID: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric flight ID.")
    results = data_manager.get_flight_by_id(id_input)
    print_results(results)


def flights_by_date(data_manager):
    while True:
        try:
            date_input = input("Enter date in DD/MM/YYYY format: ")
            date = datetime.strptime(date_input, '%d/%m/%Y')
            break
        except ValueError:
            print("Invalid format. Please try again.")
    results = data_manager.get_flights_by_date(date.day, date.month, date.year)
    print_results(results)


def print_results(results):
    if not results:
        print("No results found.")
        return

    print(f"Got {len(results)} results.")
    for result in results:
        try:
            delay = int(result['DELAY']) if result['DELAY'] else 0
            origin = result['ORIGIN_AIRPORT']
            dest = result['DESTINATION_AIRPORT']
            airline = result['AIRLINE']
            print(f"{result['FLIGHT_ID']}. {origin} -> {dest} by {airline}, Delay: {delay} Minutes")
        except (KeyError, ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results:", e)


def show_menu_and_get_input():
    options = {
        1: (flight_by_id, "Show flight by ID"),
        2: (flights_by_date, "Show flights by date"),
        3: (delayed_flights_by_airline, "Delayed flights by airline"),
        4: (delayed_flights_by_airport, "Delayed flights by origin airport"),
        5: (quit, "Exit")
    }

    while True:
        print("Menu:")
        for key, value in options.items():
            print(f"{key}. {value[1]}")
        choice = input("Choose an option: ")
        if choice.isdigit() and int(choice) in options:
            return options[int(choice)][0]


def main():
    data_manager = data.FlightData(SQLITE_URI)
    while True:
        choice_func = show_menu_and_get_input()
        choice_func(data_manager)


if __name__ == "__main__":
    main()
