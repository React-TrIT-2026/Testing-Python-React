import { seatMarks } from "../domain/schedule.js";

export function SeatMeter({ session, myStatus }) {
  const marks = seatMarks(session, myStatus);
  const taken = session.confirmed;
  const label = session.full
    ? "Completa"
    : `${session.seats_left} de ${session.capacity} libres`;

  return (
    <div className="seats">
      <div
        className="seats__pips"
        role="img"
        aria-label={`${taken} de ${session.capacity} plazas ocupadas`}
      >
        {marks.map((mark, index) => (
          <span
            key={index}
            className={`seats__pip${mark === "free" ? "" : ` seats__pip--${mark}`}`}
          />
        ))}
      </div>
      <p className="seats__count">
        <strong>{label}</strong>
        {session.waitlisted > 0 && ` · ${session.waitlisted} en espera`}
      </p>
    </div>
  );
}
