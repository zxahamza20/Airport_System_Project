import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
    return (
        <div className="home-page">
            <div className="hero-section">
                    <h1>Airport Management System</h1>
                    <p>Manage flights, bookings, and passenger itineraries</p>
                </div>
            <div className="features-grid">
                <Link to="/flight-search" className="feature-card">
                    <h3>Flight Search</h3>
                    <p>Search for flights</p>
                </Link>
                <Link to="/seat-availability" className="feature-card">
                    <h3>Seat Availability</h3>
                    <p>Check available seats on a flight</p>
                </Link>
                <Link to="/bookings" className="feature-card">
                    <h3>Book a Seat</h3>
                    <p>Reserve a seat on a flight</p>
                </Link>
                <Link to="/passenger-queries" className="feature-card">
                    <h3>My Trips</h3>
                    <p>View passenger itineraries</p>
                </Link>
                <Link to="/reports" className="feature-card">
                    <h3>Aircraft Reports</h3>
                    <p>View aircraft utilization</p>
                </Link>
            </div>
        </div>
    );
}
export default Home;