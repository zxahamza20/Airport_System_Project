import { useState } from 'react';
import './FlightSearch.css'; // Reusing search styles for consistency

export default function SeatAvailability() {
  const [flightNumber, setFlightNumber] = useState('');
  const [date, setDate] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResults(null);

    try {
      // Endpoint based on backend logic in bookings.py
      const res = await fetch(`/api/seat-availability?flight=${flightNumber}&date=${date}`);
      if (!res.ok) throw new Error('No flight instance found or server error');
      
      const data = await res.json();
      setResults(data); // Expecting array of legs with remaining capacity
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flight-search-page">
      <h2>Check Seat Availability</h2>
      <form className="flight-search-form" onSubmit={handleSubmit}>
        <input
          type="number"
          placeholder="Flight Number (e.g. 1014)"
          value={flightNumber}
          onChange={e => setFlightNumber(e.target.value)}
          required
        />
        <input
          type="date"
          value={date}
          onChange={e => setDate(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>Check</button>
      </form>

      {loading && <div className="loading">Checking capacity...</div>}
      {error && <div className="error">{error}</div>}

      {results && (
        <div className="results">
          {results.map((leg, index) => (
            <div key={index} className="result-card" style={{border: '1px solid #444', padding: '1rem', marginBottom: '1rem'}}>
              <p><strong>Leg Number:</strong> {leg.Leg_no}</p>
              <p><strong>Total Seats:</strong> {leg.Total_no_of_seats}</p>
              <p><strong>Confirmed:</strong> {leg.Confirmed_Reservations}</p>
              <p><strong>Remaining:</strong> {leg.Remaining_Capacity}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
