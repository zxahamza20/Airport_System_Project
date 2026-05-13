# Airport Management System

## 1. Environment & Technologies
* **Language:** Python 3.10+ (Developed and tested on Python 3.12)
* **Database:** MySQL 8.0+
* **Operating System:** macOS / Linux / Windows
* **Dependencies:** 
    * `mysql-connector-python`: For database connectivity
    * `pandas`: For internal data verification scripts
    * `flask`: For GUI integration

## 2. Dependencies & Installation
To install all required third-party modules, run the following command in your terminal:
```bash
pip install mysql-connector-python flask pandas
```

## 3. Project Structure
```
Airport_System_Project-main/
│
├── backend/
│   ├── __init__.py
│   ├── bookings.py
│   ├── db_connection.py
│   ├── flight_search.py
│   ├── passenger_queries.py
│   └── reports.py
│
├── database/
│   ├── airline_DB_M1.sql
│   ├── AIRPLANE_TYPE.csv
│   ├── AIRPLANE.csv
│   ├── AIRPORT.csv
│   ├── CAN_LAND.csv
│   ├── FARE.csv
│   ├── FLIGHT_LEG.csv
│   ├── FLIGHT.csv
│   ├── LEG_INSTANCE.csv
│   └── SEAT.csv
│
├── frontend/
│   ├── __init__.py
│   └── gui_placeholder.txt
│
├── main_cli.py
└── README.md
```

## 4. Database Setup

### 4.1 Initialize Schema
Execute the `database/airline_DB_M1.sql` script in your MySQL environment to create all necessary tables:
```bash
mysql -u root -p < database/airline_DB_M1.sql
```

### 4.2 Load CSV Data
The SQL script includes `LOAD DATA INFILE` statements that import data from the following CSV files located in the `database/` directory:
- `AIRPLANE_TYPE.csv`
- `AIRPLANE.csv`
- `AIRPORT.csv`
- `CAN_LAND.csv`
- `FARE.csv`
- `FLIGHT_LEG.csv`
- `FLIGHT.csv`
- `LEG_INSTANCE.csv`
- `SEAT.csv`

### 4.3 Configure Database Connection
Update the connection parameters in `backend/db_connection.py`:
```python
config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'airline_db',
    'raise_on_warnings': True
}
```

## 5. How to Build and Run the CLI

### 5.1 Build Steps
1. **Extract the archive** containing the project files
2. **Install dependencies:**
   ```bash
   pip install mysql-connector-python flask pandas
   ```
3. **Set up the database** as described in Section 4
4. **Verify database connection** by running a test query

### 5.2 Run the Application
Execute the command-line interface to test Milestone 2 functionality:
```bash
python main_cli.py
```

### 5.3 Expected Output
The CLI will present a menu with the following options:
- Flight search by route
- Flight details by number
- Seat availability check
- Passenger itinerary lookup
- Aircraft utilization reports

## 6. How to Build and Run the UI

### 6.1 Run the Frontend
'''bash
cd frontend
npm run dev'''
Accesible at http://localhost:5173/

### 6.2 Run the Backend
'''bash
python -m flask --app app run
'''

## 7. Implemented Features (Milestone 2)

### 7.1 Flight Search (`backend/flight_search.py`)
- **Direct flights:** Search for non-stop flights between two cities
  ```python
  trip("DFW", "SFO")  # Using airport codes
  trip("Dallas", "San Francisco")  # Using city names
  ```
- **One-stop itineraries:** Find connecting flights with a single layover

### 7.2 Flight Details (`backend/flight_search.py`)
- Retrieve comprehensive information by flight number:
  ```python
  flight("AA3478")  # Returns departure time, arrival, aircraft type, seat map, fares
  ```

### 7.3 Passenger Queries (`backend/passenger_queries.py`)
- **Seat availability:** Check open seats for a specific flight instance
- **Passenger itineraries:** Retrieve complete travel history for a passenger

### 7.4 Reports (`backend/reports.py`)
- **Aircraft utilization:** Generate reports showing usage statistics for a specified time period
  - Hours flown per aircraft
  - Maintenance schedules
  - Leg count per aircraft type

### 7.5 Booking System (`backend/bookings.py`)
- Reserve seats
- Process fare calculations
- Manage passenger reservations

### 8. Implemented Features (Milestone 3)
## 8.1 GUI ('frontend')
- All functions implemented via the CLI are now accessible through a gui

## 8.2 Flight Search ('frontend/src/pages/FlightSearch.jsx')
- Finds connecting flights by airports and a date

## 8.3 Infrastructure Reports ('frontend/src/pages/report.jsx')
- Reports on Airplanes and how many flights they've had for a given time period

## 8.4 Passenger and Booking Queries
### 8.4.1 Check Seat Availability ('frontend/src/pages/SeatAvailability.jsx')
- Finds seats available for a flight

### 8.4.2 Book a Seat ('frontend/src/pages/Bookings.jsx')
- Books an open seat for a flight for a person

### 8.4.3 Passenger Itinerary Retrieval ('frontend/src/pages/Itinerary.jsx')
- Takes a name and finds all booked seats for that person

## 9. Version Information
- **Python:** 3.12 
- **MySQL:** 8.0.35
- **mysql-connector-python:** 8.1.0
- **Flask:** 2.3.3 (for future GUI integration)
