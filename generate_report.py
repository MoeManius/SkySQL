import data
from datetime import datetime

# Define the SQLite database connection
SQLITE_URI = 'sqlite:///data/flights.sqlite3'

# Load the HTML template from the templates folder
TEMPLATE_FILE = "templates/template.html"
OUTPUT_FILE = "flight_report.html"


def generate_flight_report(flights):
    """
    Generates an HTML report of flight data using a template.

    :param flights: List of flight records (dictionary objects)
    """
    # Read the HTML template file
    try:
        with open(TEMPLATE_FILE, "r") as file:
            html_template = file.read()
    except FileNotFoundError:
        print(f"Error: Template file '{TEMPLATE_FILE}' not found.")
        return

    # Set the report title
    title = "Flight Delays Report"

    # Construct flight data as HTML list items
    flight_items = ""
    for flight in flights:
        flight_items += f"""
        <li class="movie">
            <div class="movie-title">{flight['FLIGHT_ID']} - {flight['ORIGIN_AIRPORT']} to {flight['DESTINATION_AIRPORT']}</div>
            <div class="movie-airline">Airline: {flight['AIRLINE']}</div>
            <div class="movie-delay">Delay: {flight['DELAY']} minutes</div>
        </li>
        """

    # Replace placeholders in the HTML template
    html_output = html_template.replace("__TEMPLATE_TITLE__", title)
    html_output = html_output.replace("__TEMPLATE_MOVIE_GRID__", flight_items)

    # Write the generated HTML to an output file
    with open(OUTPUT_FILE, "w") as output_file:
        output_file.write(html_output)

    print(f"Flight report has been generated: {OUTPUT_FILE}")


def main():
    """
    Main function to retrieve flight data and generate an HTML report.
    """
    # Initialize data access
    data_manager = data.FlightData(SQLITE_URI)

    # Prompt the user for a date to fetch flight data
    date_input = input("Enter date in DD/MM/YYYY format: ")
    try:
        date = datetime.strptime(date_input, '%d/%m/%Y')
        day, month, year = date.day, date.month, date.year
    except ValueError:
        print("Invalid date format. Please enter a valid date (DD/MM/YYYY).")
        return

    # Fetch flights for the given date
    flights = data_manager.get_flights_by_date(day, month, year)

    if flights:
        generate_flight_report(flights)
    else:
        print("No flights found for the given date.")


if __name__ == "__main__":
    main()
