from flask import Flask, jsonify, request
from flask_cors import CORS 

from backend.reports import report
from backend.passenger_queries import passenger_itinerary

from backend.db_connection import (
    connect_to_db,
    get_cursor,
    close_connection
)

app = Flask(__name__)
CORS(app) # Allows React (e.g., on port 3000) to talk to Flask (on port 5000)

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

        print(startDate, startTime, endDate, endTime, registrationNum)

        results = report(cursor, startDate, endDate, startTime, endTime)

        # If a registrationNum was provided, search the result rows (each row is a mapping)
        if registrationNum:
            for row in results:
                if str(row.get("Airplane_id")) == str(registrationNum):
                    return jsonify({
                        "message": "success",
                        "data": [row],
                    })

        # Not found (or no registrationNum provided)
        return jsonify({
            "message": f"Failed to find airplane with registration number: {registrationNum}",
            "data": results,
        })
    except Exception as e:
        print("Error in /report:", e)
        return jsonify({"message": "error", "error": str(e)}), 500
    finally:
        if conn:
            try:
                close_connection(conn)
            except Exception:
                pass

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
