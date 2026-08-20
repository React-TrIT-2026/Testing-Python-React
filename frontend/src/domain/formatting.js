const LEVEL_LABELS = {
  beginner: "Iniciación",
  intermediate: "Intermedio",
  advanced: "Avanzado",
};

const PLAN_LABELS = {
  unlimited: "Mensual ilimitado",
  ten_pass: "Bono 10 sesiones",
  pay_per_class: "Pago por sesión",
};

const STATUS_LABELS = {
  confirmed: "Confirmada",
  waitlisted: "En lista de espera",
  cancelled: "Cancelada",
  attended: "Asistida",
  no_show: "No asistió",
};

export function formatPrice(cents) {
  if (!Number.isFinite(cents)) throw new Error("El precio debe ser un número");
  return `${(cents / 100).toFixed(2).replace(".", ",")} €`;
}

export function formatTime(isoDate) {
  const date = new Date(isoDate);
  if (Number.isNaN(date.getTime())) throw new Error("Fecha no válida");
  return `${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
}

export function formatDayKey(isoDate) {
  const date = new Date(isoDate);
  if (Number.isNaN(date.getTime())) throw new Error("Fecha no válida");
  return [
    date.getFullYear(),
    String(date.getMonth() + 1).padStart(2, "0"),
    String(date.getDate()).padStart(2, "0"),
  ].join("-");
}

export function formatDayLabel(isoDate, now) {
  const key = formatDayKey(isoDate);
  if (now) {
    const today = new Date(now);
    if (key === formatDayKey(today)) return "Hoy";
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    if (key === formatDayKey(tomorrow)) return "Mañana";
  }
  return new Date(isoDate).toLocaleDateString("es-ES", {
    weekday: "long",
    day: "numeric",
    month: "long",
  });
}

export function formatDuration(minutes) {
  if (!Number.isInteger(minutes) || minutes <= 0) {
    throw new Error("La duración debe ser un entero positivo");
  }
  if (minutes < 60) return `${minutes} min`;
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  return rest === 0 ? `${hours} h` : `${hours} h ${rest} min`;
}

export function levelLabel(level) {
  return LEVEL_LABELS[level] ?? level;
}

export function planLabel(plan) {
  return PLAN_LABELS[plan] ?? plan;
}

export function statusLabel(status) {
  return STATUS_LABELS[status] ?? status;
}
