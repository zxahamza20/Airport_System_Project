import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

export default function Reports() {
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [registrationNum, setRegNum] = useState("");

  const getReport = async (event) => {
    event.preventDefault();

    const params = new URLSearchParams({
      startDate: startDate.toISOString().slice(0, 10),
      endDate: endDate.toISOString().slice(0, 10),
      registrationNum,
    });

    const res = await fetch(`http://127.0.0.1:5000/report?${params.toString()}`);
    const json = await res.json();
    console.log(json.data);
  };

  return (
    <div className="page-placeholder">
      <h2>Reports</h2>
      {/* TODO: Implement Reports page */}
      <form onSubmit={getReport}>
        <div>
          <h3>Registration Number</h3>
          <input name="registrationNum" value={registrationNum} onChange={(e) => setRegNum(e.target.value)} />
        </div>
        <div>
          <h3>Report Start Date</h3>
          <DatePicker label="Start Date" selected={startDate} onChange={(date) => setStartDate(date)} />
        </div>
        <div>
          <h3>Report End Date</h3>
          <DatePicker label="End Date" selected={endDate} onChange={(date) => setEndDate(date)} />
        </div>
        <div>
          <h3>
            <button type="submit">Submit</button>
          </h3>
        </div>
      </form>
    </div>
  );
}
