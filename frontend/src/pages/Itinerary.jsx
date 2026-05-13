import { useState } from 'react';
import './Itinerary.css';

export default function Itinerary() {
  const [name, setName] = useState('');
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError('');
    setResults(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/itinerary?name=${encodeURIComponent(name)}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed");
      }

      setResults(data.data);

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
          value={name}
          placeholder="Enter Passenger Name"
          onChange={(e) => setName(e.target.value)}
        />

        <button type="submit">
          Search
        </button>
      </form>

      {loading && <p>Searching...</p>}
      {error && <p>{error}</p>}

      {results && (
        <pre>{JSON.stringify(results, null, 2)}</pre>
      )}
    </div>
  );
}
