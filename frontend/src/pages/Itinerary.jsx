import { useState } from 'react';
import './Itinerary.css';

export default function Itinerary() {
  const [customerId, setCustomerId] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError('');
    setResults(null);

    try {
      const res = await fetch(
        `/api/itinerary?customer_id=${encodeURIComponent(customerId)}`
      );

      if (!res.ok) {
        throw new Error('Passenger not found or server error');
      }

      const data = await res.json();
      setResults(data);

    } catch (err) {
      setError(err.message);

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="itinerary-page">
      <h2>Passenger Itinerary</h2>

      <form className="itinerary-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter Customer ID"
          value={customerId}
          onChange={(e) => setCustomerId(e.target.value)}
          required
        />

        <button type="submit" disabled={loading}>
          Search
        </button>
      </form>

      {loading && <div className="loading">Searching...</div>}
      {error && <div className="error">{error}</div>}

      {results && (
        <div className="results">
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
