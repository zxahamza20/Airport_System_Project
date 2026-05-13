from flask import Flask, jsonify, request
from flask_cors import CORS 
from backend.reports import report
from backend.passenger_queries import passenger_itinerary
from backend.db_connection import connect_to_db, get_cursor, close_connection
import backend.flight_search as fs 

app = Flask(__name__)
CORS(app) 

@app.route("/")
def home():
    return {"status": "online"}

@app.route("/api/seat-availability", methods=['GET'])
def get_seats():
    flight_num = request.args.get('flight')
    date = request.args.get('date')
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT li.Leg_no, a.Total_no_of_seats, 
               COUNT(r.Seat_no) AS Confirmed_Reservations,
               (a.Total_no_of_seats - COUNT(r.Seat_no)) AS Remaining_Capacity
        FROM LEG_INSTANCE li
        JOIN AIRPLANE a ON li.Airplane_id = a.Airplane_id
        LEFT JOIN RESERVATION r ON li.Flight_number = r.Flight_number 
                                AND li.Leg_no = r.Leg_no AND li.Date = r.Date
        WHERE li.Flight_number = %s AND li.Date = %s
        GROUP BY li.Leg_no, a.Total_no_of_seats
    """
    cursor.execute(query, (flight_num, date))
    results = cursor.fetchall()
    close_connection(conn)
    return jsonify(results)

@app.route("/api/bookings", methods=['POST'])
def book_seat():
    data = request.json
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO RESERVATION (Customer_name, Flight_number, Leg_no, Date, Seat_no)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data['customerName'], data['flightNumber'], data['legNo'], data['date'], data['seatNo']))
        conn.commit()
        return jsonify({"message": "Booking successful"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        close_connection(conn)

@app.route("/api/flight-search", methods=['GET'])
def search():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    origin_codes = fs._resolve_airport_codes(cursor, origin)
    dest_codes = fs._resolve_airport_codes(cursor, destination)
    
    if not origin_codes or not dest_codes:
        return jsonify([])

    query = "SELECT * FROM FLIGHT_LEG WHERE Dep_airport_code = %s AND Arr_airport_code = %s"
    cursor.execute(query, (origin_codes[0], dest_codes[0]))
    results = cursor.fetchall()
    close_connection(conn)
    return jsonify(results)

@app.route("/api/itinerary", methods=['GET'])
def get_itinerary():
    
    customer_name = request.args.get('customer_id') 
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT r.*, fl.Dep_airport_code, fl.Arr_airport_code 
        FROM RESERVATION r
        JOIN FLIGHT_LEG fl ON r.Flight_number = fl.Flight_number AND r.Leg_no = fl.Leg_no
        WHERE r.Customer_name = %s
    """
    cursor.execute(query, (customer_name,))
    results = cursor.fetchall()
    close_connection(conn)
    return jsonify(results)

@app.route("/report", methods=['GET'])
def get_report():
    conn = connect_to_db()
    cursor = get_cursor(conn)
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    startTime = request.args.get('startTime', '00:00:00')
    endTime = request.args.get('endTime', '23:59:59')
    
    results = report(cursor, startDate, endDate, startTime, endTime)
    close_connection(conn)
    return jsonify({"data": results})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
