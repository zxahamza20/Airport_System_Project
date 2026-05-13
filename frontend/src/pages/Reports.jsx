import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

export default function Reports() {
  const [startDate, setStartDate] = useState(new Date("2025-01-01"));
  const [endDate, setEndDate] = useState(new Date());
  const [registrationNum, setRegNum] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [startTime, setStartTime] = useState("00:00");
  const [endTime, setEndTime] = useState("23:59");

  const getReport = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    const params = new URLSearchParams({
      startDate: startDate.toISOString().slice(0, 10),
      endDate: endDate.toISOString().slice(0, 10),
      startTime: `${startTime}:00`,
      endTime: `${endTime}:00`,
      registrationNum,
    });

    const res = await fetch(`http://127.0.0.1:5000/report?${params.toString()}`);
    try {
      const json = await res.json();
      setResults(json.data || []);
      console.log(json.data);
    } catch (e) {
      setError("Failed to load report");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-placeholder">
      <h2>Reports</h2>
      {/* TODO: Implement Reports page */}
      <form onSubmit={getReport}>
        <div>
          <h3>Registration Number</h3>
          <p>Leave blank for all airplanes</p>
          <input name="registrationNum" value={registrationNum} onChange={(e) => setRegNum(e.target.value)} />
        </div>
        <div>
          <h3>Report Start</h3>
          <div style={{ marginTop: 8 }}>
            <label style={{ marginRight: 8 }}>Start Date</label>
            <DatePicker label="Start Date" selected={startDate} onChange={(date) => setStartDate(date)} />
          </div>
          <div style={{ marginTop: 8 }}>
            <label style={{ marginRight: 8 }}>Start Time</label>
            <input type="time" value={startTime} onChange={(e) => setStartTime(e.target.value)} />
          </div>
          
        </div>
        <div>
          <h3>Report End</h3>
          <div style={{ marginTop: 8 }}>
            <label style={{ marginRight: 8 }}>End Date</label>
            <DatePicker label="End Date" selected={endDate} onChange={(date) => setEndDate(date)} />
          </div>
          <div style={{ marginTop: 8 }}>
            <label style={{ marginRight: 8 }}>End Time</label>
            <input type="time" value={endTime} onChange={(e) => setEndTime(e.target.value)} />
          </div>
        </div>
        <div>
          <h3>
            <button type="submit">Submit</button>
          </h3>
        </div>
      </form>

      <div style={{ marginTop: 20 }}>
        {loading && <p>Loading...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}

        {results && results.length > 0 ? (
          <table style={{ borderCollapse: 'collapse', width: '100%' }}>
            <thead>
              <tr>
                <th style={{ border: '1px solid #ddd', padding: 8 }}>Airplane ID</th>
                <th style={{ border: '1px solid #ddd', padding: 8 }}>Type</th>
                <th style={{ border: '1px solid #ddd', padding: 8 }}>Flight Count</th>
              </tr>
            </thead>
            <tbody>
              {results.map((row, idx) => (
                <tr key={idx}>
                  <td style={{ border: '1px solid #ddd', padding: 8 }}>{row.Airplane_id}</td>
                  <td style={{ border: '1px solid #ddd', padding: 8 }}>{row.Type_name}</td>
                  <td style={{ border: '1px solid #ddd', padding: 8 }}>{row.Flight_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          !loading
        )}
      </div>
    </div>
  );
}
