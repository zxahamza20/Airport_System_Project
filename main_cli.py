from backend.db_connection import ( 
    connect_to_db,
    get_cursor,
    close_connection
)
from backend.reports import report
from backend.passenger_queries import passenger_itinerary
import re

conn = connect_to_db()
cursor = get_cursor(conn)

while True:
    prompt = input("prompt> ")
    
    cmd = prompt.split('(')[0]
    args = re.findall(r'"(.*?)"', prompt)
    
    match cmd:
        case "report":
            startDate = args[0] if len(args) > 0 else '2000-01-01'
            endDate = args[1] if len(args) > 1 else '2030-01-01'
            startTime = args[2] if len(args) > 2 else '00:00:00'
            endTime = args[3] if len(args) > 3 else '23:59:59'
            
            report(cursor, startDate, endDate, startTime, endTime)
        case "exit":
            break

close_connection(conn)
