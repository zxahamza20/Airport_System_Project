def report(cursor, startDate, endDate, startTime, endTime):
    print("-- Report --")
    
    cursor.execute(
        f"""
        SELECT
	        a.Airplane_id, 
	        a.Type_name,
        COUNT(DISTINCT i.Flight_number) AS Flight_count
        FROM AIRPLANE a
        LEFT JOIN LEG_INSTANCE i ON a.Airplane_id = i.AIRPLANE_ID
        WHERE TIMESTAMP(i.Date, i.Arr_time) >= '{startDate} {startTime}' AND TIMESTAMP(i.Date, i.Dep_time) <= '{endDate} {endTime}'
        GROUP BY Airplane_id, a.Type_name;
        """
    )
    
    results = cursor.fetchall()
    print("Airplane ID\tType\tFlights")
    for airplane in results:
        print(f"{airplane['Airplane_id']}\t{airplane['Type_name']}\t{airplane['Flight_count']}")
    
    return results
