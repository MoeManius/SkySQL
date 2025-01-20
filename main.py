import data
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI environments
import matplotlib.pyplot as plt
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


def generate_flight_report(data_manager):
    """
    Generate an HTML report of flights by date.
    """
    from generate_report import generate_flight_report  # Import report function

    while True:
        try:
            date_input = input("Enter date in DD/MM/YYYY format: ")
            date = datetime.strptime(date_input, '%d/%m/%Y')
            break
        except ValueError:
            print("Invalid date format. Please enter a valid date (DD/MM/YYYY).")

    flights = data_manager.get_flights_by_date(date.day, date.month, date.year)

    if flights:
        generate_flight_report(flights)
        print("Flight report generated successfully! Check 'flight_report.html'.")
    else:
        print("No flights found for the given date.")


def plot_delayed_flights_per_airline(data_manager):
    """
    Generate a bar chart showing the percentage of delayed flights per airline.
    """
    query = """
        SELECT airlines.AIRLINE, 
               COUNT(CASE WHEN flights.DEPARTURE_DELAY >= 20 THEN 1 END) * 100.0 / COUNT(*) AS DELAY_PERCENTAGE
        FROM flights
        JOIN airlines ON flights.AIRLINE = airlines.ID
        GROUP BY airlines.AIRLINE
        ORDER BY DELAY_PERCENTAGE DESC
    """
    results = data_manager._execute_query(query, {})

    if results:
        airlines = [row['AIRLINE'] for row in results]
        percentages = [row['DELAY_PERCENTAGE'] for row in results]

        plt.figure(figsize=(10, 6))
        plt.barh(airlines, percentages, color='skyblue')
        plt.xlabel('Percentage of Delayed Flights (%)')
        plt.ylabel('Airline')
        plt.title('Percentage of Delayed Flights per Airline')
        plt.gca().invert_yaxis()  # Reverse the order for better visualization
        plt.show()
    else:
        print("No data available to generate the graph.")


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
        5: (generate_flight_report, "Generate flight report"),
        6: (plot_delayed_flights_per_airline, "Show delayed flight percentage per airline"),
        7: (quit, "Exit")
    }

    while True:
        print("\nMenu:")
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
