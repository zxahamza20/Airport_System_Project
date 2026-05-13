import { useState } from 'react';
import './FlightSearch.css';

function fmt(timeStr) {
  if (!timeStr) return '—';
  const [h, m] = timeStr.split(':').map(Number);
  const ampm = h >= 12 ? 'PM' : 'AM';
  const hour = h % 12 || 12;
  return `${hour}:${String(m).padStart(2, '0')} ${ampm}`;
}

function fmtDate(dateStr) {
  if (!dateStr) return '—';
  const [y, mo, d] = dateStr.split('-').map(Number);
  return new Date(y, mo - 1, d).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

function fmtLayover(mins) {
  if (mins == null) return '—';
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return h ? `${h}h ${m}m` : `${m}m`;
}

function LegRow({ leg, label }) {
  return (
    <div className="fs-leg">
      {label && <span className="fs-leg-label">{label}</span>}

      <div className="fs-leg-body">
        <div className="fs-route">
          <span className="fs-code">{leg.dep_airport}</span>
          <span className="fs-arrow">→</span>
          <span className="fs-code">{leg.arr_airport}</span>
        </div>

        <div className="fs-meta">
          <span className="fs-badge">{leg.airline}</span>
          <span className="fs-badge secondary">#{leg.flight_number}</span>
        </div>

        <div className="fs-times">
          <div className="fs-time-block">
            <span className="fs-time-label">Departs</span>
            <span className="fs-time-val">{fmt(leg.dep_time)}</span>
          </div>

          <div className="fs-time-divider" />

          <div className="fs-time-block">
            <span className="fs-time-label">Arrives</span>
            <span className="fs-time-val">{fmt(leg.arr_time)}</span>
          </div>

          <div className="fs-time-block right">
            <span className="fs-time-label">Date</span>
            <span className="fs-time-val small">{fmtDate(leg.date)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function DirectCard({ flight }) {
  return (
    <div className="fs-card">
      <div className="fs-card-type direct">Direct</div>
      <LegRow leg={flight} />
    </div>
  );
}

function ConnectingCard({ conn }) {
  return (
    <div className="fs-card">
      <div className="fs-card-type connecting">Connecting</div>

      <LegRow leg={conn.leg1} label="Leg 1" />

      <div className="fs-layover">
        <span className="fs-layover-dot" />
        <span className="fs-layover-text">
          Layover at <strong>{conn.leg1.arr_airport}</strong>
          &nbsp;·&nbsp;{fmtLayover(conn.layover_minutes)}
        </span>
        <span className="fs-layover-dot" />
      </div>

      <LegRow leg={conn.leg2} label="Leg 2" />
    </div>
  );
}

function FlightDetailCard({ data }) {
  const legs = data?.legs ?? [];

  return (
    <div className="fs-card">
      <div className="fs-card-header-row">
        <span className="fs-badge large">{data.airline}</span>
        <span className="fs-badge large secondary">
          Flight #{data.flight_number}
        </span>
      </div>

      {legs.map((leg) => (
        <LegRow
          key={leg.leg_no}
          leg={{
            ...leg,
            airline: data.airline,
            flight_number: data.flight_number,
          }}
          label={legs.length > 1 ? `Leg ${leg.leg_no}` : null}
        />
      ))}
    </div>
  );
}

function EmptyState({ message }) {
  return (
    <div className="fs-empty">
      <svg viewBox="0 0 48 48" fill="none" aria-hidden="true">
        <path
          d="M6 36l10-14 8 6 10-16 8 10"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <circle cx="40" cy="8" r="4" stroke="currentColor" strokeWidth="2" />
      </svg>
      <p>{message}</p>
    </div>
  );
}

export default function FlightSearch() {
  const [tab, setTab] = useState('route');

  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [routeDate, setRouteDate] = useState('');
  const [routeResults, setRouteResults] = useState(null);

  const [flightNum, setFlightNum] = useState('');
  const [flightDate, setFlightDate] = useState('');
  const [flightResult, setFlightResult] = useState(null);

  const [routeLoading, setRouteLoading] = useState(false);
  const [flightLoading, setFlightLoading] = useState(false);
  const [error, setError] = useState('');

  const direct = routeResults?.direct ?? [];
  const connecting = routeResults?.connecting ?? [];

  const handleRouteSearch = async (e) => {
    e.preventDefault();
    setRouteLoading(true);
    setError('');
    setRouteResults(null);

    try {
      const params = new URLSearchParams({
        origin,
        destination,
        date: routeDate,
      });

      const res = await fetch(`/api/flight-search?${params}`);
      if (!res.ok) throw new Error(await res.text());

      const data = await res.json();
      setRouteResults(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setRouteLoading(false);
    }
  };

  const handleFlightLookup = async (e) => {
    e.preventDefault();
    setFlightLoading(true);
    setError('');
    setFlightResult(null);

    try {
      const params = new URLSearchParams({
        flightNumber: flightNum,
        date: flightDate,
      });

      const res = await fetch(`/api/flight-details?${params}`);
      if (!res.ok) throw new Error(await res.text());

      const data = await res.json();
      setFlightResult(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setFlightLoading(false);
    }
  };

  const totalCount = direct.length + connecting.length;

  return (
    <div className="fs-root">
      <header className="fs-header">
        <div className="fs-header-icon">✈</div>
        <div>
          <h1 className="fs-title">Flight Search</h1>
          <p className="fs-subtitle">Airline database query interface</p>
        </div>
      </header>

      <div className="fs-tabs">
        <button
          className={`fs-tab ${tab === 'route' ? 'active' : ''}`}
          onClick={() => {
            setTab('route');
            setError('');
            setFlightResult(null);
          }}
        >
          Route Search
        </button>

        <button
          className={`fs-tab ${tab === 'flight' ? 'active' : ''}`}
          onClick={() => {
            setTab('flight');
            setError('');
            setRouteResults(null);
          }}
        >
          Flight Lookup
        </button>
      </div>

      {tab === 'route' && (
        <form className="fs-form" onSubmit={handleRouteSearch}>
          <div className="fs-field-group">
            <input
              className="fs-input code-input"
              placeholder="Origin (DFW)"
              value={origin}
              onChange={(e) => setOrigin(e.target.value.toUpperCase())}
              required
            />

            <input
              className="fs-input code-input"
              placeholder="Destination (LAX)"
              value={destination}
              onChange={(e) => setDestination(e.target.value.toUpperCase())}
              required
            />

            <input
              className="fs-input"
              type="date"
              value={routeDate}
              onChange={(e) => setRouteDate(e.target.value)}
              required
            />
          </div>

          <button className="fs-btn" disabled={routeLoading}>
            {routeLoading ? 'Searching…' : 'Search Flights'}
          </button>
        </form>
      )}

      {tab === 'flight' && (
        <form className="fs-form" onSubmit={handleFlightLookup}>
          <div className="fs-field-group">
            <input
              className="fs-input code-input"
              placeholder="Flight Number"
              value={flightNum}
              onChange={(e) => setFlightNum(e.target.value)}
              required
            />

            <input
              className="fs-input"
              type="date"
              value={flightDate}
              onChange={(e) => setFlightDate(e.target.value)}
              required
            />
          </div>

          <button className="fs-btn" disabled={flightLoading}>
            {flightLoading ? 'Looking up…' : 'Look Up Flight'}
          </button>
        </form>
      )}

      {error && <div className="fs-error">{error}</div>}

      {tab === 'route' && routeResults && (
        <section className="fs-results">
          {totalCount === 0 ? (
            <EmptyState
              message={`No flights found from ${origin} to ${destination}.`}
            />
          ) : (
            <>
              <div className="fs-results-header">
                {totalCount} flights found
              </div>

              {direct.length > 0 && (
                <>
                  <h2>Direct</h2>
                  {direct.map((f, i) => (
                    <DirectCard key={i} flight={f} />
                  ))}
                </>
              )}

              {connecting.length > 0 && (
                <>
                  <h2>Connecting</h2>
                  {connecting.map((c, i) => (
                    <ConnectingCard key={i} conn={c} />
                  ))}
                </>
              )}
            </>
          )}
        </section>
      )}

      {tab === 'flight' && flightResult && (
        <section className="fs-results">
          {!flightResult?.legs?.length ? (
            <EmptyState message="No flight details found." />
          ) : (
            <FlightDetailCard data={flightResult} />
          )}
        </section>
      )}
    </div>
  );
}