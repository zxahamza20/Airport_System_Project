from flask import Flask, jsonify, request
from flask_cors import CORS 

from backend.reports import report

from backend.db_connection import (
    connect_to_db,
    get_cursor,
    close_connection
)

from backend.reports import report

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
        registrationNum = request.args.get('registrationNum')
        
        print(startDate, endDate, registrationNum)

        results = report(cursor, startDate, endDate, '00:00:00', '23:59:59')

        return jsonify({
            "message": "success",
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
