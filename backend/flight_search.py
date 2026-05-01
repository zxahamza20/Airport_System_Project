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
            return [r[0] for r in rows]

    cursor.execute(
        "SELECT Airport_code FROM AIRPORT "
        "WHERE City LIKE %s OR Name LIKE %s OR State LIKE %s",
        (f"%{q}%", f"%{q}%", f"%{q}%"),
    )
    rows = cursor.fetchall()
    return [r[0] for r in rows]


def _airport_label(cursor, code: str) -> str:
    cursor.execute(
        "SELECT Name, City, State FROM AIRPORT WHERE Airport_code = %s",
        (code,),
    )
    row = cursor.fetchone()
    if row:
        return f"{code} – {row[0]}, {row[1]}, {row[2]}"
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
                fn, airline, weekdays, leg, dep, arr, dep_t, arr_t = row
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
                (
                    f1,
                    al1,
                    d1,
                    l1,
                    dep1,
                    via,
                    dt1,
                    at1,
                    f2,
                    al2,
                    d2,
                    l2,
                    dep2,
                    arr2,
                    dt2,
                    at2,
                ) = row

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

        num, airline, weekdays = flight

        print(f"\n{'═' * 65}")
        print(f" FLIGHT #{num}  |  {airline}  |  Operates: {weekdays}")
        print(f"{'═' * 65}")

        cursor.execute(
            """
            SELECT fl.Leg_no,
                fl.Dep_airport_code, adep.Name, adep.City,
                fl.Arr_airport_code, aarr.Name, aarr.City,
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
            lg, dc, dn, dcity, ac, an, acity, dep_t, arr_t = leg
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
            for code, amount, restrictions in fares:
                print(
                    f"  [{code}]  ${amount:>8.2f}  |  "
                    f"{restrictions or 'No restrictions'}"
                )

        print(f"\n{'═' * 65}\n")

    finally:
        cursor.close()
        conn.close()