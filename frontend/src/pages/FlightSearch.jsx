import { useState } from 'react';
import './FlightSearch.css';

function fmt(timeStr) {
  if (!timeStr) return '—';
  const [h, m] = timeStr.split(':').map(Number);
  const ampm = h >= 12 ? 'PM' : 'AM';
  const hour = h % 12 || 12;
  return `${hour}:${String(m).padStart(2, '0')} ${ampm}`;
}

/** "2024-01-15"  →  "Jan 15, 2024" */
function fmtDate(dateStr) {
  if (!dateStr) return '—';
  // Parse as local date (avoid UTC shift from new Date(dateStr))
  const [y, mo, d] = dateStr.split('-').map(Number);
  return new Date(y, mo - 1, d).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
  });
}

/** minutes  →  "1h 35m" */
function fmtLayover(mins) {
  if (!mins && mins !== 0) return '—';
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return h ? `${h}h ${m}m` : `${m}m`;
}

// ── Sub-components ────────────────────────────

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
  return (
    <div className="fs-card">
      <div className="fs-card-header-row">
        <span className="fs-badge large">{data.airline}</span>
        <span className="fs-badge large secondary">Flight #{data.flight_number}</span>
      </div>
      {data.legs.map((leg) => (
        <LegRow
          key={leg.leg_no}
          leg={{ ...leg, airline: data.airline, flight_number: data.flight_number }}
          label={data.legs.length > 1 ? `Leg ${leg.leg_no}` : null}
        />
      ))}
    </div>
  );
}

function EmptyState({ message }) {
  return (
    <div className="fs-empty">
      <svg viewBox="0 0 48 48" fill="none" aria-hidden="true">
        <path d="M6 36l10-14 8 6 10-16 8 10" stroke="currentColor" strokeWidth="2"
          strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="40" cy="8" r="4" stroke="currentColor" strokeWidth="2" />
      </svg>
      <p>{message}</p>
    </div>
  );
}

// ── Main Component ────────────────────────────

export default function FlightSearch() {
  const [tab, setTab] = useState('route'); // 'route' | 'flight'

  // Route search state
  const [origin, setOrigin]           = useState('');
  const [destination, setDestination] = useState('');
  const [routeDate, setRouteDate]     = useState('');
  const [routeResults, setRouteResults] = useState(null); // { direct, connecting }

  // Flight lookup state
  const [flightNum, setFlightNum]     = useState('');
  const [flightDate, setFlightDate]   = useState('');
  const [flightResult, setFlightResult] = useState(null); // { flight_number, airline, legs }

  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState('');

  // ── Route Search Submit ──
  const handleRouteSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setRouteResults(null);
    try {
      const params = new URLSearchParams({ origin, destination, date: routeDate });
      const res = await fetch(`/api/flight-search?${params}`);
      if (!res.ok) {
        const msg = await res.text().catch(() => 'Server error');
        throw new Error(msg || `HTTP ${res.status}`);
      }
      const data = await res.json();
      setRouteResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // ── Flight Lookup Submit ──
  const handleFlightLookup = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setFlightResult(null);
    try {
      const params = new URLSearchParams({ flightNumber: flightNum, date: flightDate });
      const res = await fetch(`/api/flight-details?${params}`);
      if (!res.ok) {
        const msg = await res.text().catch(() => 'Server error');
        throw new Error(msg || `HTTP ${res.status}`);
      }
      const data = await res.json();
      setFlightResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // ── Count helpers ──
  const directCount     = routeResults?.direct?.length     ?? 0;
  const connectingCount = routeResults?.connecting?.length ?? 0;
  const totalCount      = directCount + connectingCount;

  return (
    <div className="fs-root">

      {/* ── Header ── */}
      <header className="fs-header">
        <div className="fs-header-icon" aria-hidden="true">✈</div>
        <div>
          <h1 className="fs-title">Flight Search</h1>
          <p className="fs-subtitle">Airline database query interface</p>
        </div>
      </header>

      {/* ── Tabs ── */}
      <div className="fs-tabs" role="tablist">
        <button
          role="tab"
          aria-selected={tab === 'route'}
          className={`fs-tab ${tab === 'route' ? 'active' : ''}`}
          onClick={() => { setTab('route'); setError(''); setFlightResult(null); }}
        >
          Route Search
        </button>
        <button
          role="tab"
          aria-selected={tab === 'flight'}
          className={`fs-tab ${tab === 'flight' ? 'active' : ''}`}
          onClick={() => { setTab('flight'); setError(''); setRouteResults(null); }}
        >
          Flight Lookup
        </button>
      </div>

      {/* ── Route Search Form ── */}
      {tab === 'route' && (
        <form className="fs-form" onSubmit={handleRouteSearch} noValidate>
          <div className="fs-field-group">
            <div className="fs-field">
              <label htmlFor="origin" className="fs-label">Origin</label>
              <input
                id="origin"
                className="fs-input code-input"
                type="text"
                placeholder="e.g. DFW"
                maxLength={3}
                value={origin}
                onChange={e => setOrigin(e.target.value.toUpperCase())}
                required
                aria-label="Origin airport code"
              />
            </div>
            <div className="fs-swap-icon" aria-hidden="true">⇄</div>
            <div className="fs-field">
              <label htmlFor="destination" className="fs-label">Destination</label>
              <input
                id="destination"
                className="fs-input code-input"
                type="text"
                placeholder="e.g. LAX"
                maxLength={3}
                value={destination}
                onChange={e => setDestination(e.target.value.toUpperCase())}
                required
                aria-label="Destination airport code"
              />
            </div>
            <div className="fs-field date-field">
              <label htmlFor="routeDate" className="fs-label">Date</label>
              <input
                id="routeDate"
                className="fs-input"
                type="date"
                value={routeDate}
                onChange={e => setRouteDate(e.target.value)}
                required
                aria-label="Travel date"
              />
            </div>
          </div>
          <button className="fs-btn" type="submit" disabled={loading}>
            {loading ? <span className="fs-spinner" aria-hidden="true" /> : null}
            {loading ? 'Searching…' : 'Search Flights'}
          </button>
        </form>
      )}

      {/* ── Flight Lookup Form ── */}
      {tab === 'flight' && (
        <form className="fs-form" onSubmit={handleFlightLookup} noValidate>
          <div className="fs-field-group">
            <div className="fs-field">
              <label htmlFor="flightNum" className="fs-label">Flight Number</label>
              <input
                id="flightNum"
                className="fs-input code-input"
                type="text"
                placeholder="e.g. 3478"
                value={flightNum}
                onChange={e => setFlightNum(e.target.value)}
                required
                aria-label="Flight number"
              />
            </div>
            <div className="fs-field date-field">
              <label htmlFor="flightDate" className="fs-label">Date</label>
              <input
                id="flightDate"
                className="fs-input"
                type="date"
                value={flightDate}
                onChange={e => setFlightDate(e.target.value)}
                required
                aria-label="Flight date"
              />
            </div>
          </div>
          <button className="fs-btn" type="submit" disabled={loading}>
            {loading ? <span className="fs-spinner" aria-hidden="true" /> : null}
            {loading ? 'Looking up…' : 'Look Up Flight'}
          </button>
        </form>
      )}

      {/* ── Error ── */}
      {error && (
        <div className="fs-error" role="alert">
          <span aria-hidden="true">⚠</span> {error}
        </div>
      )}

      {/* ── Route Results ── */}
      {tab === 'route' && routeResults && (
        <section className="fs-results" aria-label="Search results">
          {totalCount === 0 ? (
            <EmptyState message={`No flights found from ${origin} to ${destination} on ${fmtDate(routeDate)}.`} />
          ) : (
            <>
              <div className="fs-results-header">
                <span className="fs-results-count">
                  {totalCount} flight{totalCount !== 1 ? 's' : ''} found
                </span>
                <span className="fs-results-meta">
                  {origin} → {destination} · {fmtDate(routeDate)}
                </span>
              </div>

              {/* Direct flights */}
              {directCount > 0 && (
                <div className="fs-section">
                  <h2 className="fs-section-title">
                    Direct <span className="fs-pill">{directCount}</span>
                  </h2>
                  {routeResults.direct.map((f, i) => (
                    <DirectCard key={`direct-${i}`} flight={f} />
                  ))}
                </div>
              )}

              {/* Connecting flights */}
              {connectingCount > 0 && (
                <div className="fs-section">
                  <h2 className="fs-section-title">
                    Connecting <span className="fs-pill">{connectingCount}</span>
                  </h2>
                  {routeResults.connecting.map((conn, i) => (
                    <ConnectingCard key={`conn-${i}`} conn={conn} />
                  ))}
                </div>
              )}
            </>
          )}
        </section>
      )}

      {/* ── Flight Lookup Result ── */}
      {tab === 'flight' && flightResult && (
        <section className="fs-results" aria-label="Flight details">
          {!flightResult.legs || flightResult.legs.length === 0 ? (
            <EmptyState message={`No details found for flight #${flightNum} on ${fmtDate(flightDate)}.`} />
          ) : (
            <>
              <div className="fs-results-header">
                <span className="fs-results-count">Flight details</span>
              </div>
              <FlightDetailCard data={flightResult} />
            </>
          )}
        </section>
      )}

    </div>
  );
}