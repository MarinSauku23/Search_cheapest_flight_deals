import time
from data_manager import DataManager
from flight_data import find_cheapest_flight
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

datamanager = DataManager()
flightsearch = FlightSearch()
notification_manager = NotificationManager()

sheet_data = datamanager.get_sheet_data()

ORIGIN_CITY_IATA = "BOS"

for city_row in sheet_data:
    if city_row['iataCode'] == "":
        city_row["iataCode"] = flightsearch.get_iata_codes(city_row["city"])

        time.sleep(2)

print(f"sheet_data:\n {sheet_data}")

datamanager.sheet_data = sheet_data
datamanager.put_sheet_data()

customer_data = datamanager.get_customer_email()
customer_email_list = [row["whatIsYourEmail?"] for row in customer_data]

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flightsearch.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")

    time.sleep(2)

    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        stopover_flights = flightsearch.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct=False
        )
        cheapest_flight = find_cheapest_flight(stopover_flights)
        print(f"Cheapest indirect flight price is: ${cheapest_flight.price}")


    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only USD {cheapest_flight.price} to fly direct "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only USD {cheapest_flight.price} to fly " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"with {cheapest_flight.stops} stop(s) " \
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        print(f"Check your email. Lower price flight found to {destination['city']}!")

        notification_manager.send_emails(email_list=customer_email_list, email_body=message)
