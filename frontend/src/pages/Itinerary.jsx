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
        `http://127.0.0.1:5000/api/itinerary?name=${encodeURIComponent(name)}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed");
      }
      console.log(data);

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
        <div className="results">
          {results.map((result, index) => (
            <div key={index} className="result-card" style={{border: '1px solid #444', padding: '1rem', marginBottom: '1rem'}}>
              <h3>{result.Flight_number}</h3>
              <p>From: {result.Dep_airport_code}</p>
              <p>To: {result.Arr_airport_code}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
