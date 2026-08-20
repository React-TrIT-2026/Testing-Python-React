export const WEEK_TARGET = 3;

export function attendedByWeek(bookings, classes) {
  const weeks = new Map();
  for (const booking of bookings) {
    if (booking.status !== "attended") continue;
    const session = classes.find((c) => c.id === booking.class_id);
    if (!session) continue;
    const key = isoWeekKey(session.starts_at);
    weeks.set(key, (weeks.get(key) ?? 0) + 1);
  }
  return weeks;
}

export function isoWeekKey(isoDate) {
  const date = new Date(isoDate);
  if (Number.isNaN(date.getTime())) throw new Error("Fecha no válida");
  const thursday = new Date(date);
  thursday.setDate(date.getDate() + 3 - ((date.getDay() + 6) % 7));
  const firstThursday = new Date(thursday.getFullYear(), 0, 4);
  const week =
    1 +
    Math.round(
      (thursday - firstThursday) / 604_800_000 - ((firstThursday.getDay() + 6) % 7) / 7,
    );
  return `${thursday.getFullYear()}-W${String(week).padStart(2, "0")}`;
}

export function currentStreak(weeks, weekKeys) {
  let streak = 0;
  for (const key of weekKeys) {
    if ((weeks.get(key) ?? 0) >= WEEK_TARGET) streak += 1;
    else break;
  }
  return streak;
}

export function progressLabel(attended, target = WEEK_TARGET) {
  if (attended < 0) throw new Error("Las asistencias no pueden ser negativas");
  if (attended >= target) return "Objetivo cumplido";
  const missing = target - attended;
  return missing === 1 ? "Te falta 1 clase" : `Te faltan ${missing} clases`;
}
