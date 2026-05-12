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
          {/* Render results here. Structure depends on backend API response. */}
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
