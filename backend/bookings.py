from backend.db_connection import connect_to_db, close_connection
import argparse

def check_seat_availability(flight_number, flight_date):
    conn = connect_to_db()
    if not conn:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                li.Flight_number,
                li.Leg_no,
                li.Date,
                a.Total_no_of_seats,
                COUNT(r.Seat_no) AS Confirmed_Reservations,
                (a.Total_no_of_seats - COUNT(r.Seat_no)) AS Remaining_Capacity
            FROM 
                LEG_INSTANCE li
            JOIN 
                AIRPLANE a ON li.Airplane_id = a.Airplane_id
            LEFT JOIN 
                RESERVATION r ON li.Flight_number = r.Flight_number 
                              AND li.Leg_no = r.Leg_no 
                              AND li.Date = r.Date
            WHERE 
                li.Flight_number = %s AND li.Date = %s
            GROUP BY 
                li.Flight_number, li.Leg_no, li.Date, a.Total_no_of_seats
            ORDER BY
                li.Leg_no;
        """

        cursor.execute(query, (flight_number, flight_date))
        results = cursor.fetchall()

        if not results:
            print(f"No flight instance found for Flight {flight_number} on {flight_date}.")
        else:
            print(f"\n--- Seat Availability for Flight {flight_number} on {flight_date} ---")
            for row in results:
                print(f"Leg Number:             {row['Leg_no']}")
                print(f"Total Airplane Seats:   {row['Total_no_of_seats']}")
                print(f"Confirmed Reservations: {row['Confirmed_Reservations']}")
                print(f"Remaining Capacity:     {row['Remaining_Capacity']}")
                print("-" * 45)

    except Exception as e:
        print(f"An error occurred while checking seat availability: {e}")
        
    finally:
        if cursor:
            cursor.close()
        close_connection(conn)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check seat availability for a flight.")
    
    parser.add_argument("flight", type=int, help="The flight number (e.g., 1014)")
    parser.add_argument("date", type=str, help="The flight date (YYYY-MM-DD)")

    args = parser.parse_args()

    check_seat_availability(args.flight, args.date)
