import { useEffect } from "react";
import { ClassCard } from "../components/ClassCard.jsx";
import { DayGroup } from "../components/DayGroup.jsx";
import { EmptyState } from "../components/EmptyState.jsx";
import { bookingFor, groupByDay } from "../domain/schedule.js";


export function ScheduleBoard({
  classes,
  bookings,
  member,
  now,
  onBook,
  onCancel,
  pendingClassId,
  pendingBookingId,
}) {
  if (classes.length === 0) {
    return (
      <EmptyState title="No hay clases programadas">
        <p>Cuando el estudio publique el próximo cuadrante, aparecerá aquí.</p>
      </EmptyState>
    );
  }

  return (
    <div className="reveal">
      {groupByDay(classes).map(({ day, sessions }) => (
        <DayGroup key={day} day={day} sessions={sessions} now={now}>
          {(session) => {
            const booking = bookingFor(bookings, session.id);
            const busy =
              pendingClassId === session.id ||
              (booking != null && pendingBookingId === booking.id);
            return (
              <ClassCard
                session={session}
                booking={booking}
                member={member}
                now={now}
                busy={busy}
                onBook={onBook}
                onCancel={onCancel}
              />
            );
          }}
        </DayGroup>
      ))}
    </div>
  );
}
