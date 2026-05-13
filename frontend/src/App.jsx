import { Routes, Route, Link, Navigate } from 'react-router-dom';
import FlightSearch from './pages/FlightSearch';
import Bookings from './pages/Bookings';
import Itinerary from './pages/Itinerary';
import Reports from './pages/Reports';
import SeatAvailability from './pages/SeatAvailability';
import './App.css';
import Home from './pages/Home';

function App() {
  return (
    <div className="app dark-mode">
      <nav className="navbar">
        <h1 className="logo">Airport System</h1>
        <ul className="nav-links">
          <li><Link to="/home">Home</Link></li>
          <li><Link to="/flight-search">Flight Search</Link></li>
          <li><Link to="/seat-availability">Seat Availability</Link></li>
          <li><Link to="/bookings">Bookings</Link></li>
          <li><Link to="/passenger-queries">Passenger Queries</Link></li>
          <li><Link to="/reports">Reports</Link></li>
        </ul>
      </nav>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Navigate to="/home" />} />
          <Route path="/home" element={<Home />} />
          <Route path="/flight-search" element={<FlightSearch />} />
          <Route path="/seat-availability" element={<SeatAvailability />} />
          <Route path="/bookings" element={<Bookings />} />
          <Route path="/passenger-queries" element={<Itinerary />} />          
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
