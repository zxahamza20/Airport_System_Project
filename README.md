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
- http://localhost:5173/flight-search
- Finds connecting flights by airports and a date

## 8.3 Infrastructure Reports ('frontend/src/pages/report.jsx')
- http://localhost:5173/reports
- Reports on Airplanes and how many flights they've had for a given time period

## 8.4 Passenger and Booking Queries
### 8.4.1 Check Seat Availability ('frontend/src/pages/SeatAvailability.jsx')
- http://localhost:5173/seat-availability
- Finds seats available for a flight

### 8.4.2 Book a Seat ('frontend/src/pages/Bookings.jsx')
- http://localhost:5173/bookings
- Books an open seat for a flight for a person

### 8.4.3 Passenger Itinerary Retrieval ('frontend/src/pages/Itinerary.jsx')
- http://localhost:5173/passenger-queries
- Takes a name and finds all booked seats for that person

## 9. Version Information
- **Python:** 3.12 
- **MySQL:** 8.0.35
- **mysql-connector-python:** 8.1.0
- **Flask:** 2.3.3 (for future GUI integration)

### 10. Design Patterns & Architecture
## 10.1 Architectural Choice: Decoupled Client-Server
The system follows a Client-Server Architecture. We chose to decouple the frontend (React) from the backend (Flask) to ensure a separation of concerns. The Flask API acts as a "Thin Controller," handling database transactions and business logic, while React manages the State and View. This allows the UI to be highly responsive, updating dynamically without page reloads.

## 10.2 Design Decisions
Programming Language: Python was selected for the backend due to its robust support for data manipulation (Pandas) and seamless MySQL integration. JavaScript (JSX) was chosen for the frontend to leverage the React ecosystem for modern UI components.

GUI Framework: React was chosen over traditional templates (like Jinja2) because it allows for a "Single Page Application" (SPA) feel. Our menus are designed using Action Cards on the Home screen rather than complex nested dropdowns to ensure the system is intuitive for airport staff who need to perform tasks quickly.

Schema Design: We augmented the basic schema with a specific RESERVATION table logic that connects LEG_INSTANCE and SEAT data, allowing for real-time seat tracking.

## 10.3 Data Access Pattern
We implemented the Data Access Object (DAO) pattern via db_connection.py. By centralizing connection logic, we ensure that database handles are opened and closed correctly, preventing memory leaks and "too many connections" errors in MySQL.

## 11. Quick Start Guide
To perform common tasks in the system, follow these steps:

Check Seat Availability:

- Click Seat Availability on the Home dashboard.

- Enter the Flight Number (e.g., 1014) and Date.

- The system will display total seats vs. confirmed bookings and calculate the remaining capacity.

Make a New Booking:

- Go to Book a Seat.

- Fill in the passenger name and flight details.

-Click Confirm Booking to update the database.

Note: Ensure the Seat Number matches the format in the database (e.g., 12A).

View Passenger Trips:

- Go to My Trips.

- Enter the name of the passenger.

- The system fetches all associated flight legs, showing the departure and arrival airports for that specific traveler.

Run Aircraft Utilization Report:

- Go to Aircraft Reports.

- Select a date range (Start and End).

- Click Submit. The system will generate a table showing how many flights each aircraft in the fleet performed during that window.
