from backend.db_connection import connect_to_db, close_connection
import argparse


def passenger_itinerary(customer_name):
    conn = connect_to_db()

    if not conn:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                r.Customer_name,
                r.Flight_number,
                r.Leg_no,
                r.Date,
                fl.Dep_airport_code,
                fl.Arr_airport_code,
                fl.Scheduled_dep_time,
                fl.Scheduled_arr_time,
                r.Seat_no
            FROM RESERVATION r
            JOIN FLIGHT_LEG fl
                ON r.Flight_number = fl.Flight_number
                AND r.Leg_no = fl.Leg_no
            WHERE r.Customer_name = %s
            ORDER BY r.Date, r.Flight_number, r.Leg_no;
        """

        cursor.execute(query, (customer_name,))
        results = cursor.fetchall()

        if not results:
            print(f"No itinerary found for {customer_name}.")
        else:
            print(f"\n--- Itinerary for {customer_name} ---")

            for row in results:
                print(f"Flight Number: {row['Flight_number']}")
                print(f"Leg Number:    {row['Leg_no']}")
                print(f"Date:          {row['Date']}")
                print(f"Route:         {row['Dep_airport_code']} -> {row['Arr_airport_code']}")
                print(f"Departure:     {row['Scheduled_dep_time']}")
                print(f"Arrival:       {row['Scheduled_arr_time']}")
                print(f"Seat:          {row['Seat_no']}")
                print("-" * 45)

    except Exception as e:
        print(f"An error occurred while retrieving itinerary: {e}")

    finally:
        if cursor:
            cursor.close()
        close_connection(conn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Retrieve passenger itinerary."
    )

    parser.add_argument(
        "name",
        type=str,
        help="Passenger name (e.g., John Smith)"
    )

    args = parser.parse_args()

    passenger_itinerary(args.name)
