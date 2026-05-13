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
CORS(app)  # Allows React to talk to Flask


@app.route("/")
def hello_world():
    return {}


@app.route("/report", methods=['GET'])
def get_report():
    conn = None

    try:
        conn = connect_to_db()
        cursor = get_cursor(conn)

        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')
        startTime = request.args.get('startTime', '00:00:00')
        endTime = request.args.get('endTime', '23:59:59')
        registrationNum = request.args.get('registrationNum')

        results = report(cursor, startDate, endDate, startTime, endTime)

        if registrationNum:
            for row in results:
                if str(row.get("Airplane_id")) == str(registrationNum):
                    return jsonify({
                        "message": "success",
                        "data": [row]
                    })

        return jsonify({
            "message": "success",
            "data": results
        })

    except Exception as e:
        print("Error in /report:", e)

        return jsonify({
            "message": "error",
            "error": str(e)
        }), 500

    finally:
        if conn:
            close_connection(conn)


@app.route("/itinerary", methods=['GET'])
def get_itinerary():

    try:
        customer_name = request.args.get('name')

        results = passenger_itinerary(customer_name)

        return jsonify({
            "message": "success",
            "data": results
        })

    except Exception as e:
        print("Error in /itinerary:", e)

        return jsonify({
            "message": "error",
            "error": str(e)
        }), 500


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
    app.run(debug=True)
