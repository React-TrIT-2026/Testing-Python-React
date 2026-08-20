const LEVEL_RANK = { beginner: 0, intermediate: 1, advanced: 2 };

export const BLOCK_REASONS = {
  no_member: "Elige un socio para poder reservar.",
  dues_unpaid: "Cuota pendiente",
  blocked: "Reservas bloqueadas",
  level_too_low: "Pide más nivel",
  already_started: "Ya ha empezado",
  outside_window: "Aún no se puede reservar",
  no_credits: "Sin sesiones en el bono",
};

export const MAX_DAYS_AHEAD = 14;

export function bookingBlockReason(member, session, now) {
  if (!member) return "no_member";
  if (!member.dues_paid) return "dues_unpaid";
  if (member.blocked_until && new Date(now) < new Date(member.blocked_until)) {
    return "blocked";
  }
  if (LEVEL_RANK[member.level] < LEVEL_RANK[session.min_level]) {
    return "level_too_low";
  }

  const startsAt = new Date(session.starts_at);
  const reference = new Date(now);
  if (startsAt <= reference) return "already_started";
  if (startsAt - reference > MAX_DAYS_AHEAD * 86_400_000) return "outside_window";

  if (member.plan === "ten_pass" && member.credits <= 0 && !session.full) {
    return "no_credits";
  }
  return null;
}

export function blockLabel(reason) {
  return reason ? (BLOCK_REASONS[reason] ?? "No disponible") : null;
}
