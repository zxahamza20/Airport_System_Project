import { useState } from 'react';
import './FlightSearch.css';

export default function Bookings() {
  const [formData, setFormData] = useState({
    customerName: '',
    flightNumber: '',
    legNo: '1',
    date: '',
    seatNo: ''
  });
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const res = await fetch('/api/bookings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (res.ok) {
        setMessage(`Success! Seat ${formData.seatNo} reserved for ${formData.customerName}.`);
        setFormData({ customerName: '', flightNumber: '', legNo: '1', date: '', seatNo: '' });
      } else {
        throw new Error(data.error || 'Failed to book seat');
      }
    } catch (err) {
      setMessage(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flight-search-page">
      <h2>Reserve a Seat</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <input
          type="text"
          placeholder="Passenger Name"
          value={formData.customerName}
          onChange={e => setFormData({...formData, customerName: e.target.value})}
          required
        />
        <div style={{ display: 'flex', gap: '1rem' }}>
          <input
            type="number"
            placeholder="Flight #"
            style={{ flex: 2 }}
            value={formData.flightNumber}
            onChange={e => setFormData({...formData, flightNumber: e.target.value})}
            required
          />
          <input
            type="number"
            placeholder="Leg #"
            style={{ flex: 1 }}
            value={formData.legNo}
            onChange={e => setFormData({...formData, legNo: e.target.value})}
            required
          />
        </div>
        <input
          type="date"
          value={formData.date}
          onChange={e => setFormData({...formData, date: e.target.value})}
          required
        />
        <input
          type="text"
          placeholder="Seat Number (e.g. 14A)"
          value={formData.seatNo}
          onChange={e => setFormData({...formData, seatNo: e.target.value})}
          required
        />
        <button type="submit" disabled={loading} style={{
          padding: '0.75rem', 
          background: '#c084fc', 
          color: '#181a20', 
          fontWeight: 'bold', 
          cursor: 'pointer'
        }}>
          {loading ? 'Processing...' : 'Confirm Booking'}
        </button>
      </form>
      
      {message && (
        <div className={message.startsWith('Error') ? 'error' : 'success'} style={{ marginTop: '1rem' }}>
          {message}
        </div>
      )}
    </div>
  );
}
