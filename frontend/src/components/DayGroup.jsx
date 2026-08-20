import { formatDayLabel, formatDuration, formatTime } from "../domain/formatting.js";

export function DayGroup({ day, sessions, now, children }) {
  const openCount = sessions.filter((s) => !s.full).length;

  return (
    <section className="daygroup" aria-label={formatDayLabel(day, now)}>
      <header className="daygroup__heading">
        <h2 className="daygroup__day">{formatDayLabel(day, now)}</h2>
        <p className="daygroup__meta">
          {sessions.length} {sessions.length === 1 ? "clase" : "clases"} · {openCount} con
          plaza
        </p>
      </header>

      <ul>
        {sessions.map((session) => (
          <li key={session.id} className="rail">
            <p className="rail__time">
              {formatTime(session.starts_at)}
              <span className="rail__duration">{formatDuration(session.duration_min)}</span>
            </p>
            <div>{children(session)}</div>
          </li>
        ))}
      </ul>
    </section>
  );
}
