import { useState } from 'react';
import './FlightSearch.css';

export default function FlightSearch() {
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResults(null);
    try {
      // Replace with your backend API endpoint
      const res = await fetch(`/api/flight-search?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}`);
      if (!res.ok) throw new Error('No results or server error');
      const data = await res.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flight-search-page">
      <h2>Flight Search</h2>
      <form className="flight-search-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Origin (city, code, etc)"
          value={origin}
          onChange={e => setOrigin(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Destination (city, code, etc)"
          value={destination}
          onChange={e => setDestination(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>Search</button>
      </form>
      {loading && <div className="loading">Searching...</div>}
      {error && <div className="error">{error}</div>}
      {results && (
        <div className="results">
          <section>
            <h3>Direct Flights ({results.direct?.length ?? 0})</h3>
            {results.direct?.length === 0 && <p className="none">No direct flights found.</p>}
            {results.direct?.map((f, i) => (
              <div key={i} className="flight-card">
                <span className="flight-num">Flight {f.flight_num}</span>
                <span className="airline">[{f.airline}]</span>
                <span>{f.dep} → {f.arr}</span>
                <span className="time">{f.dep_time} → {f.arr_time}</span>
                <span className="days">Days: {f.weekdays}</span>
              </div>
            ))}
          </section>
          <section>
            <h3>One-Stop Connections ({results.connections?.length ?? 0})</h3>
            {results.connections?.length === 0 && <p className="none">No connections found.</p>}
            {results.connections?.map((c, i) => (
              <div key={i} className="flight-card connection">
                <div>
                  <span className="flight-num">Flight {c.flight1}</span>
                  <span className="airline">[{c.airline1}]</span>
                  <span>{c.dep1} → {c.via}</span>
                  <span className="time">{c.dep_time1} → {c.arr_time1}</span>
                </div>
                <div className="connector">↓ connect at {c.via}</div>
                <div>
                  <span className="flight-num">Flight {c.flight2}</span>
                  <span className="airline">[{c.airline2}]</span>
                  <span>{c.dep2} → {c.arr2}</span>
                  <span className="time">{c.dep_time2} → {c.arr_time2}</span>
                </div>
              </div>
            ))}
          </section>
        </div>
      )}
    </div>
  );
}
