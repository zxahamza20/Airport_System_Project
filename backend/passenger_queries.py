from backend.db_connection import connect_to_db, close_connection


def passenger_itinerary(customer_name):
    conn = connect_to_db()

    if not conn:
        return {"error": "Failed to connect to database"}

    cursor = None

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

        return results

    except Exception as e:
        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()
        close_connection(conn)
