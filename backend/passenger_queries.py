from backend.db_connection import (
    connect_to_db,
    get_cursor,
    close_connection
)

def passenger_itinerary(customer_name):
    conn = connect_to_db()

    if not conn:
        return []

    cursor = get_cursor(conn)

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

    close_connection(conn)

    return results
