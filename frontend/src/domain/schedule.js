import { formatDayKey } from "./formatting.js";

export function groupByDay(classes) {
  const days = new Map();
  for (const session of [...classes].sort(
    (a, b) => new Date(a.starts_at) - new Date(b.starts_at),
  )) {
    const key = formatDayKey(session.starts_at);
    if (!days.has(key)) days.set(key, []);
    days.get(key).push(session);
  }
  return [...days.entries()].map(([day, sessions]) => ({ day, sessions }));
}

export function seatMarks(session, myBookingStatus) {
  const capacity = Math.max(0, session.capacity);
  const taken = Math.min(capacity, Math.max(0, session.confirmed));
  const mine = myBookingStatus === "confirmed" || myBookingStatus === "attended" ? 1 : 0;
  return Array.from({ length: capacity }, (_, index) => {
    if (index < mine) return "mine";
    return index < taken ? "taken" : "free";
  });
}

export function scarcity(session) {
  if (session.seats_left === 0) return "full";
  if (session.seats_left <= 2) return "few";
  return "open";
}

export function summarise(classes, bookings) {
  const active = bookings.filter(
    (b) => b.status === "confirmed" || b.status === "waitlisted",
  );
  return {
    classCount: classes.length,
    openCount: classes.filter((c) => !c.full).length,
    myBookings: active.length,
  };
}

export function bookingFor(bookings, classId) {
  return (
    bookings.find(
      (b) =>
        b.class_id === classId &&
        (b.status === "confirmed" || b.status === "waitlisted" || b.status === "attended"),
    ) ?? null
  );
}
