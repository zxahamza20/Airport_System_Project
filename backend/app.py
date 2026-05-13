from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.db_connection import connect_to_db
from backend.flight_search import _resolve_airport_codes, _format_time

app = Flask(__name__)
CORS(app)

@app.route('/api/flight-search')
def flight_search():
    origin = request.args.get('origin', '').strip()
    destination = request.args.get('destination', '').strip()

    if not origin or not destination:
        return jsonify({'error': 'Origin and destination are required'}), 400

    conn = connect_to_db()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        origin_codes = _resolve_airport_codes(cursor, origin)
        dest_codes = _resolve_airport_codes(cursor, destination)

        if not origin_codes:
            return jsonify({'error': f"No airport found matching '{origin}'"}), 404
        if not dest_codes:
            return jsonify({'error': f"No airport found matching '{destination}'"}), 404

        # Direct flights
        direct_sql = """
            SELECT f.Number, f.Airline, f.Weekdays,
                   fl.Leg_no, fl.Dep_airport_code, fl.Arr_airport_code,
                   fl.Scheduled_dep_time, fl.Scheduled_arr_time
            FROM FLIGHT f
            JOIN FLIGHT_LEG fl ON fl.Flight_number = f.Number
            WHERE fl.Dep_airport_code IN ({origins})
              AND fl.Arr_airport_code IN ({dests})
            ORDER BY fl.Scheduled_dep_time
        """.format(
            origins=','.join(['%s'] * len(origin_codes)),
            dests=','.join(['%s'] * len(dest_codes)),
        )
        cursor.execute(direct_sql, origin_codes + dest_codes)
        direct = [
            {
                'flight_num': r[0], 'airline': r[1], 'weekdays': r[2],
                'leg': r[3], 'dep': r[4], 'arr': r[5],
                'dep_time': _format_time(r[6]), 'arr_time': _format_time(r[7]),
            }
            for r in cursor.fetchall()
        ]

        # One-stop connections
        connect_sql = """
            SELECT f1.Number, f1.Airline, f1.Weekdays,
                   fl1.Dep_airport_code, fl1.Arr_airport_code,
                   fl1.Scheduled_dep_time, fl1.Scheduled_arr_time,
                   f2.Number, f2.Airline, f2.Weekdays,
                   fl2.Dep_airport_code, fl2.Arr_airport_code,
                   fl2.Scheduled_dep_time, fl2.Scheduled_arr_time
            FROM FLIGHT_LEG fl1
            JOIN FLIGHT f1 ON f1.Number = fl1.Flight_number
            JOIN FLIGHT_LEG fl2 ON fl2.Dep_airport_code = fl1.Arr_airport_code
            JOIN FLIGHT f2 ON f2.Number = fl2.Flight_number
            WHERE fl1.Dep_airport_code IN ({origins})
              AND fl2.Arr_airport_code IN ({dests})
              AND fl1.Arr_airport_code NOT IN ({origins})
              AND fl1.Arr_airport_code NOT IN ({dests})
              AND fl2.Scheduled_dep_time > fl1.Scheduled_arr_time
            ORDER BY fl1.Scheduled_dep_time, fl2.Scheduled_dep_time
            LIMIT 50
        """.format(
            origins=','.join(['%s'] * len(origin_codes)),
            dests=','.join(['%s'] * len(dest_codes)),
        )
        cursor.execute(connect_sql, origin_codes + dest_codes + origin_codes + dest_codes)
        connections = [
            {
                'flight1': r[0], 'airline1': r[1], 'weekdays1': r[2],
                'dep1': r[3], 'via': r[4],
                'dep_time1': _format_time(r[5]), 'arr_time1': _format_time(r[6]),
                'flight2': r[7], 'airline2': r[8], 'weekdays2': r[9],
                'dep2': r[10], 'arr2': r[11],
                'dep_time2': _format_time(r[12]), 'arr_time2': _format_time(r[13]),
            }
            for r in cursor.fetchall()
        ]

        return jsonify({
            'origin_codes': origin_codes,
            'dest_codes': dest_codes,
            'direct': direct,
            'connections': connections,
        })

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)