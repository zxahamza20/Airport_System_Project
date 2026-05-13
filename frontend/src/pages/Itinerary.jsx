import { useState } from 'react';
import './Itinerary.css';

export default function Itinerary() {
  const [name, setName] = useState('');
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
        `/api/itinerary?name=${encodeURIComponent(name)}`
      );

      if (!res.ok) {
        throw new Error('No itinerary found');
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
          placeholder="Enter Passenger Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <button type="submit">
          Search
        </button>
      </form>

      {loading && <p>Searching...</p>}
      {error && <p>{error}</p>}

      {results && (
        <pre>
          {JSON.stringify(results, null, 2)}
        </pre>
      )}

    </div>
  );
}
```

