export const FREE_CANCELLATION_HOURS = 12;
export const NO_REFUND_HOURS = 2;

export const CANCELLATION_BANDS = {
  free: { label: "Cancelación libre", tone: "free" },
  late: { label: "Cancelación tardía", tone: "late" },
  no_refund: { label: "Sin devolución", tone: "norefund" },
};

export function hoursUntil(startsAt, now) {
  return (new Date(startsAt).getTime() - new Date(now).getTime()) / 3_600_000;
}

export function cancellationBand(startsAt, now) {
  const margin = hoursUntil(startsAt, now);
  if (margin >= FREE_CANCELLATION_HOURS) return "free";
  if (margin >= NO_REFUND_HOURS) return "late";
  return "no_refund";
}

export function describeCancellation(startsAt, now) {
  const band = cancellationBand(startsAt, now);
  return { band, ...CANCELLATION_BANDS[band] };
}
