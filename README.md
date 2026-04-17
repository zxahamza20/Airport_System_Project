# Airport Management System - Milestone 2
**CS-4347: Database Systems** 

## 1. Environment & Technologies
* **Language:** Python 3.10+ 
* **Database:** MySQL 
* **Web Framework:** Flask (Backend logic for Milestone 2; GUI integration for Milestone 3)
* **Dependencies:** `mysql-connector-python`, `flask` 

## 2. Project Structure
The project follows a modular architecture to separate database logic from the user interface.
* `database/schema.sql`: Contains `CREATE TABLE` statements and data loading scripts.
* `backend/`: Contains Python modules for flight searches, reports, and bookings.
* `main_cli.py`: The command-line interface for testing Milestone 2 functionality.
* `app.py`: The Flask entry point (to be fully integrated in Milestone 3).

## 3. Database Setup
1.  **Initialize Schema:** Execute the `database/schema.sql` file in your MySQL environment to create the tables.
2.  **Data Loading:** Ensure the `.csv` source files are located in the path specified within the `LOAD DATA` statements of the SQL script.
3.  **Connection:** Configure your credentials in `backend/db_connection.py`.

## 4. How to Run & Build
Milestone 2 logic is executed via the command line.
1.  **Install dependencies:**
    ```bash
    pip install mysql-connector-python flask
    ```
2.  **Run the CLI Tester:**
    ```bash
    python main_cli.py
    ```

## 5. Functional Requirements (Milestone 2)
The following features are implemented as Python functions that interact with the MySQL backend:
* **Flight Search:** Supports searching for direct and one-stop itineraries using city names or three-letter codes (e.g., `trip("DFW", "SFO")`).
* **Flight Details:** Retrieves specific details via flight number (e.g., `flight("AA3478")`).
* **Infrastructure Reports:** Generates Aircraft Utilization reports based on a given time period.
* [**Passenger Queries:** Checks seat availability for specific flight instances and retrieves full passenger itineraries.
