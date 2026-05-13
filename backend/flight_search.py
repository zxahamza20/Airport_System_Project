from backend.db_connection import connect_to_db

def _resolve_airport_codes(cursor, query: str) -> list[str]:
    q = query.strip()
    if not q:
        return []

    q_upper = q.upper()
    if len(q_upper) == 3 and q_upper.isalpha():
        cursor.execute(
            "SELECT Airport_code FROM AIRPORT WHERE Airport_code = %s",
            (q_upper,),
        )
        rows = cursor.fetchall()
        if rows:
            return [r['Airport_code'] for r in rows]

    cursor.execute(
        "SELECT Airport_code FROM AIRPORT "
        "WHERE City LIKE %s OR Name LIKE %s OR State LIKE %s",
        (f"%{q}%", f"%{q}%", f"%{q}%"),
    )
    rows = cursor.fetchall()
    return [r['Airport_code'] for r in rows]


def _airport_label(cursor, code: str) -> str:
    cursor.execute(
        "SELECT Name, City, State FROM AIRPORT WHERE Airport_code = %s",
        (code,),
    )
    row = cursor.fetchone()
    if row:
        return f"{code} – {row['Name']}, {row['City']}, {row['State']}"
    return code


def _format_time(t) -> str:
    """timedelta (MySQL TIME) → HH:MM string."""
    if t is None:
        return "N/A"
    total_seconds = int(t.total_seconds()) if hasattr(t, "total_seconds") else 0
    h, rem = divmod(total_seconds, 3600)
    m, _ = divmod(rem, 60)
    return f"{h:02d}:{m:02d}"


def search_itinerary(origin: str, destination: str) -> None:
    conn = connect_to_db()
    if conn is None:
        print("Database connection failed.")
        return

    cursor = conn.cursor()

    try:
        origin_codes = _resolve_airport_codes(cursor, origin)
        dest_codes = _resolve_airport_codes(cursor, destination)

        if not origin_codes:
            print(f" No airport found matching '{origin}'.")
            return
        if not dest_codes:
            print(f" No airport found matching '{destination}'.")
            return

        print(f"\n{'═' * 65}")
        print(" ITINERARY SEARCH")
        print(f" From : {', '.join(origin_codes)} ({origin})")
        print(f" To   : {', '.join(dest_codes)} ({destination})")
        print(f"{'═' * 65}")

        direct_sql = """
            SELECT
                f.Number AS flight_num,
                f.Airline,
                f.Weekdays,
                fl.Leg_no,
                fl.Dep_airport_code,
                fl.Arr_airport_code,
                fl.Scheduled_dep_time,
                fl.Scheduled_arr_time
            FROM FLIGHT f
            JOIN FLIGHT_LEG fl ON fl.Flight_number = f.Number
            WHERE fl.Dep_airport_code IN ({origins})
              AND fl.Arr_airport_code IN ({dests})
            ORDER BY fl.Scheduled_dep_time
        """.format(
            origins=",".join(["%s"] * len(origin_codes)),
            dests=",".join(["%s"] * len(dest_codes)),
        )
        cursor.execute(direct_sql, origin_codes + dest_codes)
        direct_flights = cursor.fetchall()

        print(f"\n DIRECT FLIGHTS ({len(direct_flights)} found)")
        print(f"  {'-' * 61}")

        if not direct_flights:
            print(" No direct flights found.")
        else:
            for row in direct_flights:
                fn = row['Number']
                airline = row['Airline']
                weekdays = row['Weekdays']
                leg = row['Leg_no']
                dep = row['Dep_airport_code']
                arr = row['Arr_airport_code']
                dep_t = row['Scheduled_dep_time']
                arr_t = row['Scheduled_arr_time']
                print(
                    f" Flight {fn:>6}  [{airline}]  Leg {leg}"
                    f" | {dep} → {arr}"
                    f" | {_format_time(dep_t)} → {_format_time(arr_t)}"
                    f" | Days: {weekdays}"
                )

        connect_sql = """
            SELECT
                f1.Number AS flight1,
                f1.Airline AS airline1,
                f1.Weekdays AS days1,
                fl1.Leg_no AS leg1,
                fl1.Dep_airport_code AS dep1,
                fl1.Arr_airport_code AS via,
                fl1.Scheduled_dep_time AS dep_time1,
                fl1.Scheduled_arr_time AS arr_time1,

                f2.Number AS flight2,
                f2.Airline AS airline2,
                f2.Weekdays AS days2,
                fl2.Leg_no AS leg2,
                fl2.Dep_airport_code AS dep2,
                fl2.Arr_airport_code AS arr2,
                fl2.Scheduled_dep_time AS dep_time2,
                fl2.Scheduled_arr_time AS arr_time2
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
            origins=",".join(["%s"] * len(origin_codes)),
            dests=",".join(["%s"] * len(dest_codes)),
        )
        params = origin_codes + dest_codes + origin_codes + dest_codes
        cursor.execute(connect_sql, params)
        connections = cursor.fetchall()

        print(f"\n ONE STOP CONNECTIONS  ({len(connections)} found)")
        print(f"  {'-' * 61}")

        if not connections:
            print(" No one stop connections found.")
        else:
            prev_via = None
            for row in connections:
                f1 = row['flight1']
                al1 = row['airline1']
                d1 = row['days1']
                l1 = row['leg1']
                dep1 = row['dep1']
                via = row['via']
                dt1 = row['dep_time1']
                at1 = row['arr_time1']
                f2 = row['flight2']
                al2 = row['airline2']
                d2 = row['days2']
                l2 = row['leg2']
                dep2 = row['dep2']
                arr2 = row['arr2']
                dt2 = row['dep_time2']
                at2 = row['arr_time2']

                if via != prev_via:
                    print(f"\n Connecting through {_airport_label(cursor, via)}")
                    prev_via = via

                print(
                    f" Leg 1 -> Flight {f1:>6} [{al1}]  "
                    f"{dep1} -> {via}  "
                    f" | {_format_time(dt1)} -> {_format_time(at1)}  Days: {d1}"
                )
                print(
                    f" Leg 2 -> Flight {f2:>6} [{al2}]  "
                    f"{dep2} -> {arr2}  "
                    f" | {_format_time(dt2)} -> {_format_time(at2)}  Days: {d2}"
                )
                print()

        print(f"{'═' * 65}\n")

    finally:
        cursor.close()
        conn.close()


def get_flight_by_number(flight_number: int) -> None:
    conn = connect_to_db()
    if conn is None:
        print("Database connection failed.")
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT Number, Airline, Weekdays FROM FLIGHT WHERE Number = %s",
            (flight_number,),
        )
        flight = cursor.fetchone()

        if not flight:
            print(f"\n Flight {flight_number} not found.")
            return

        num = flight['Number']
        airline = flight['Airline']
        weekdays = flight['Weekdays']

        print(f"\n{'═' * 65}")
        print(f" FLIGHT #{num}  |  {airline}  |  Operates: {weekdays}")
        print(f"{'═' * 65}")

        cursor.execute(
            """
            SELECT fl.Leg_no,
                fl.Dep_airport_code, adep.Name AS dep_name, adep.City AS dep_city,
                fl.Arr_airport_code, aarr.Name AS arr_name, aarr.City AS arr_city,
                fl.Scheduled_dep_time, fl.Scheduled_arr_time
            FROM FLIGHT_LEG fl
            JOIN AIRPORT adep ON adep.Airport_code = fl.Dep_airport_code
            JOIN AIRPORT aarr ON aarr.Airport_code = fl.Arr_airport_code
            WHERE fl.Flight_number = %s
            ORDER BY fl.Leg_no
            """,
            (flight_number,),
        )
        legs = cursor.fetchall()

        print(f"\n  ROUTE  ({len(legs)} leg{'s' if len(legs) != 1 else ''})")
        print(f"  {'-' * 61}")
        for leg in legs:
            lg = leg['Leg_no']
            dc = leg['Dep_airport_code']
            dn = leg['dep_name']
            dcity = leg['dep_city']
            ac = leg['Arr_airport_code']
            an = leg['arr_name']
            acity = leg['arr_city']
            dep_t = leg['Scheduled_dep_time']
            arr_t = leg['Scheduled_arr_time']
            print(
                f" Leg {lg}: {dc} ({dn}, {dcity})"
                f" ->  {ac} ({an}, {acity})"
            )
            print(
                f" Departs {_format_time(dep_t)}"
                f" | Arrives {_format_time(arr_t)}"
            )

        cursor.execute(
            "SELECT Code, Amount, Restrictions FROM FARE "
            "WHERE Flight_number = %s ORDER BY Amount",
            (flight_number,),
        )
        fares = cursor.fetchall()

        print(f"\n  FARES  ({len(fares)} class{'es' if len(fares) != 1 else ''})")
        print(f"  {'-' * 61}")
        if not fares:
            print(" No fare information available.")
        else:
            for fare in fares:
                code = fare['Code']
                amount = fare['Amount']
                restrictions = fare['Restrictions']
                print(
                    f"  [{code}]  ${amount:>8.2f}  |  "
                    f"{restrictions or 'No restrictions'}"
                )

        print(f"\n{'═' * 65}\n")

    finally:
        cursor.close()
        conn.close()


def search_flights_by_route(cursor, origin: str, destination: str, date: str) -> dict:
    """
    Search flights by origin, destination, and date.
    Returns a dict with 'direct' and 'connecting' flight lists.
    """
    try:
        origin_codes = _resolve_airport_codes(cursor, origin)
        dest_codes = _resolve_airport_codes(cursor, destination)

        if not origin_codes:
            return {"direct": [], "connecting": []}
        if not dest_codes:
            return {"direct": [], "connecting": []}

        # Direct flights - join with LEG_INSTANCE to filter by date
        direct_sql = """
            SELECT
                f.Number AS flight_number,
                f.Airline AS airline,
                fl.Leg_no,
                fl.Dep_airport_code AS dep_airport,
                fl.Arr_airport_code AS arr_airport,
                fl.Scheduled_dep_time,
                fl.Scheduled_arr_time,
                li.Date AS leg_date
            FROM FLIGHT f
            JOIN FLIGHT_LEG fl ON fl.Flight_number = f.Number
            JOIN LEG_INSTANCE li ON li.Flight_number = f.Number AND li.Leg_no = fl.Leg_no
            WHERE fl.Dep_airport_code IN ({origins})
              AND fl.Arr_airport_code IN ({dests})
              AND li.Date = %s
            ORDER BY fl.Scheduled_dep_time
        """.format(
            origins=",".join(["%s"] * len(origin_codes)),
            dests=",".join(["%s"] * len(dest_codes)),
        )
        
        cursor.execute(direct_sql, origin_codes + dest_codes + [date])
        direct_flights = cursor.fetchall()

        # Format direct flights for JSON
        direct_results = []
        for row in direct_flights:
            direct_results.append({
                "flight_number": row.get("flight_number"),
                "airline": row.get("airline"),
                "leg_no": row.get("Leg_no"),
                "dep_airport": row.get("dep_airport"),
                "arr_airport": row.get("arr_airport"),
                "dep_time": _format_time(row.get("Scheduled_dep_time")),
                "arr_time": _format_time(row.get("Scheduled_arr_time")),
                "date": str(row.get("leg_date"))
            })

        return {
            "direct": direct_results,
            "connecting": []
        }

    except Exception as e:
        print(f"Error in search_flights_by_route: {e}")
        import traceback
        traceback.print_exc()
        return {"direct": [], "connecting": []}


def get_flight_details(cursor, flight_number: str, date: str) -> dict:
    """Get details for a specific flight including legs and fares."""
    try:
        cursor.execute(
            "SELECT Number, Airline, Weekdays FROM FLIGHT WHERE Number = %s",
            (flight_number,),
        )
        flight = cursor.fetchone()

        if not flight:
            return None

        num = flight.get("Number")
        airline = flight.get("Airline")
        weekdays = flight.get("Weekdays")

        # Get flight legs
        cursor.execute(
            """
            SELECT fl.Leg_no,
                fl.Dep_airport_code, adep.Name AS dep_name, adep.City AS dep_city,
                fl.Arr_airport_code, aarr.Name AS arr_name, aarr.City AS arr_city,
                fl.Scheduled_dep_time, fl.Scheduled_arr_time
            FROM FLIGHT_LEG fl
            JOIN AIRPORT adep ON adep.Airport_code = fl.Dep_airport_code
            JOIN AIRPORT aarr ON aarr.Airport_code = fl.Arr_airport_code
            WHERE fl.Flight_number = %s
            ORDER BY fl.Leg_no
            """,
            (flight_number,),
        )
        legs = cursor.fetchall()

        legs_data = []
        for leg in legs:
            legs_data.append({
                "leg_no": leg.get("Leg_no"),
                "dep_airport": leg.get("Dep_airport_code"),
                "dep_airport_name": leg.get("dep_name"),
                "dep_city": leg.get("dep_city"),
                "arr_airport": leg.get("Arr_airport_code"),
                "arr_airport_name": leg.get("arr_name"),
                "arr_city": leg.get("arr_city"),
                "dep_time": _format_time(leg.get("Scheduled_dep_time")),
                "arr_time": _format_time(leg.get("Scheduled_arr_time")),
                "date": date
            })

        # Get fares
        cursor.execute(
            "SELECT Code, Amount, Restrictions FROM FARE "
            "WHERE Flight_number = %s ORDER BY Amount",
            (flight_number,),
        )
        fares = cursor.fetchall()

        fares_data = []
        for fare in fares:
            fares_data.append({
                "code": fare.get("Code"),
                "amount": fare.get("Amount"),
                "restrictions": fare.get("Restrictions") or "No restrictions"
            })

        return {
            "flight_number": num,
            "airline": airline,
            "weekdays": weekdays,
            "legs": legs_data,
            "fares": fares_data
        }

    except Exception as e:
        print(f"Error in get_flight_details: {e}")
        return None