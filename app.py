from flask import Flask, jsonify, request
from flask_cors import CORS 
from backend.reports import report
from backend.passenger_queries import passenger_itinerary
from backend.flight_search import search_flights_by_route, get_flight_details

from backend.db_connection import (
    connect_to_db,
    get_cursor,
    close_connection
)

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
    cursor = get_cursor(conn)
    try:
        Airplane_id_query = """
            SELECT * FROM LEG_INSTANCE
            WHERE Flight_number = %s AND Leg_no = %s and Date = %s
        """
        cursor.execute(Airplane_id_query, (data['flightNumber'], data['legNo'], data['date']))
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Leg instance not found"}), 404
        Airplane_id = row['Airplane_id']
        
        query = """
            INSERT INTO RESERVATION (Airplane_id, Customer_name, Flight_number, Leg_no, Date, Seat_no)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (Airplane_id, data['customerName'], data['flightNumber'], data['legNo'], data['date'], data['seatNo']))
        conn.commit()
        return jsonify({"message": "Booking successful"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        close_connection(conn)
        
@app.route("/api/itinerary", methods=['GET'])
def get_itinerary():
    
    customer_name = request.args.get('name')
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
    registrationNum = request.args.get('registrationNum')
    
    results = report(cursor, startDate, endDate, startTime, endTime)
    close_connection(conn)
    
    # Limit selection to registration number if provided
    if registrationNum:
            for row in results:
                if str(row.get("Airplane_id")) == str(registrationNum):
                    return jsonify({
                        "message": "success",
                        "data": [row],
                    })
    
    return jsonify({"data": results})

@app.route("/api/flight-search", methods=['GET'])
def api_flight_search():
    """Search flights by origin, destination, and date"""
    try:
        origin = request.args.get('origin', '').strip()
        destination = request.args.get('destination', '').strip()
        date = request.args.get('date', '').strip()

        if not origin or not destination or not date:
            return jsonify({
                "message": "error",
                "error": "Missing required parameters: origin, destination, date"
            }), 400

        conn = connect_to_db()
        if not conn:
            return jsonify({
                "message": "error",
                "error": "Database connection failed"
            }), 500

        cursor = get_cursor(conn)
        result = search_flights_by_route(cursor, origin, destination, date)
        close_connection(conn)

        return jsonify({
            "message": "success",
            "data": result
        })

    except Exception as e:
        print("Error in /api/flight-search:", e)
        return jsonify({
            "message": "error",
            "error": str(e)
        }), 500


@app.route("/api/flight-details", methods=['GET'])
def api_flight_details():
    """Get details for a specific flight"""
    try:
        flight_number = request.args.get('flightNumber', '').strip()
        date = request.args.get('date', '').strip()

        if not flight_number or not date:
            return jsonify({
                "message": "error",
                "error": "Missing required parameters: flightNumber, date"
            }), 400

        conn = connect_to_db()
        if not conn:
            return jsonify({
                "message": "error",
                "error": "Database connection failed"
            }), 500

        cursor = get_cursor(conn)
        result = get_flight_details(cursor, flight_number, date)
        close_connection(conn)

        return jsonify({
            "message": "success",
            "data": result
        })

    except Exception as e:
        print("Error in /api/flight-details:", e)
        return jsonify({
            "message": "error",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
