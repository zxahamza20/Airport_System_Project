# Airport Management System - Milestone 2
[cite_start]**CS-4347: Database Systems** [cite: 2]

## 1. Environment & Technologies
* [cite_start]**Language:** Python 3.10+ [cite: 12]
* [cite_start]**Database:** MySQL [cite: 13]
* **Web Framework:** Flask (Backend logic for Milestone 2; GUI integration for Milestone 3)
* [cite_start]**Dependencies:** `mysql-connector-python`, `flask` [cite: 16, 17]

## 2. Project Structure
The project follows a modular architecture to separate database logic from the user interface.
* `database/schema.sql`: Contains `CREATE TABLE` statements and data loading scripts.
* `backend/`: Contains Python modules for flight searches, reports, and bookings.
* [cite_start]`main_cli.py`: The command-line interface for testing Milestone 2 functionality[cite: 21].
* [cite_start]`app.py`: The Flask entry point (to be fully integrated in Milestone 3)[cite: 8].

## 3. Database Setup
1.  [cite_start]**Initialize Schema:** Execute the `database/schema.sql` file in your MySQL environment to create the tables[cite: 36, 37].
2.  **Data Loading:** Ensure the `.csv` source files are located in the path specified within the `LOAD DATA` statements of the SQL script.
3.  **Connection:** Configure your credentials in `backend/db_connection.py`.

## 4. How to Run & Build
[cite_start]Milestone 2 logic is executed via the command line[cite: 21].
1.  **Install dependencies:**
    ```bash
    pip install mysql-connector-python flask
    ```
2.  **Run the CLI Tester:**
    ```bash
    python main_cli.py
    ```

## 5. Functional Requirements (Milestone 2)
[cite_start]The following features are implemented as Python functions that interact with the MySQL backend[cite: 4, 11]:
* [cite_start]**Flight Search:** Supports searching for direct and one-stop itineraries using city names or three-letter codes (e.g., `trip("DFW", "SFO")`)[cite: 24, 25, 26].
* [cite_start]**Flight Details:** Retrieves specific details via flight number (e.g., `flight("AA3478")`)[cite: 27, 28].
* [cite_start]**Infrastructure Reports:** Generates Aircraft Utilization reports based on a given time period[cite: 30].
* [cite_start]**Passenger Queries:** Checks seat availability for specific flight instances and retrieves full passenger itineraries[cite: 34, 35].
