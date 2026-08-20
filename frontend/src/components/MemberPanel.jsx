import { formatTime, planLabel, statusLabel, levelLabel } from "../domain/formatting.js";

export function MemberPanel({
  members,
  member,
  bookings,
  classes,
  onSelectMember,
  onCancel,
  pendingBookingId,
}) {
  const active = bookings.filter(
    (b) => b.status === "confirmed" || b.status === "waitlisted",
  );

  return (
    <aside className="panel" aria-label="Tu ficha de socio">
      <div className="field">
        <label htmlFor="member-picker">Socio</label>
        <select
          id="member-picker"
          value={member?.id ?? ""}
          onChange={(event) => onSelectMember(Number(event.target.value))}
        >
          {members.map((option) => (
            <option key={option.id} value={option.id}>
              {option.name}
            </option>
          ))}
        </select>
      </div>

      {member && (
        <>
          <dl>
            <div className="panel__row">
              <dt>Tarifa</dt>
              <dd>{planLabel(member.plan)}</dd>
            </div>
            <div className="panel__row">
              <dt>Nivel</dt>
              <dd>{levelLabel(member.level)}</dd>
            </div>
            <div className="panel__row">
              <dt>Cuota</dt>
              <dd>{member.dues_paid ? "Al día" : "Pendiente"}</dd>
            </div>
            {member.plan === "ten_pass" && (
              <div className="panel__row">
                <dt>Sesiones</dt>
                <dd>{member.credits} de 10</dd>
              </div>
            )}
          </dl>

          {member.plan === "ten_pass" && (
            <div
              className="punchcard"
              role="img"
              aria-label={`${member.credits} sesiones disponibles de 10`}
            >
              {Array.from({ length: 10 }, (_, index) => (
                <span
                  key={index}
                  className={`punchcard__hole${
                    index < member.credits ? " punchcard__hole--left" : ""
                  }`}
                />
              ))}
            </div>
          )}

          {!member.dues_paid && (
            <p className="notice notice--error" role="alert">
              Tienes la cuota pendiente. Pasa por recepción para volver a reservar.
            </p>
          )}

          <h3 className="panel__title">Tus reservas</h3>
          {active.length === 0 ? (
            <p className="booking__when">Todavía no tienes ninguna reserva.</p>
          ) : (
            <ul>
              {active.map((booking) => {
                const session = classes.find((c) => c.id === booking.class_id);
                return (
                  <li key={booking.id} className="booking">
                    <div>
                      <p>{session?.name ?? `Clase ${booking.class_id}`}</p>
                      <p className="booking__when">
                        {session ? formatTime(session.starts_at) : "—"} ·{" "}
                        {statusLabel(booking.status)}
                      </p>
                    </div>
                    <button
                      type="button"
                      className="btn btn--ghost"
                      disabled={pendingBookingId === booking.id}
                      onClick={() => onCancel(booking)}
                    >
                      {pendingBookingId === booking.id ? "…" : "Cancelar"}
                    </button>
                  </li>
                );
              })}
            </ul>
          )}
        </>
      )}
    </aside>
  );
}
