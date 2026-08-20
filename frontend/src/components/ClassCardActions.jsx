import { describeCancellation } from "../domain/cancellation.js";
import { blockLabel } from "../domain/eligibility.js";

import { Tag } from "./Tag.jsx";

function bookLabel({ busy, full }) {
  if (busy) return "Reservando…";
  return full ? "Lista de espera" : "Reservar";
}

export function ClassCardActions({
  session,
  booking,
  now,
  blockReason,
  busy,
  onBook,
  onCancel,
}) {
  const cancellation = describeCancellation(session.starts_at, now);
  const waitlisted = booking?.status === "waitlisted";

  return (
    <div className="card__actions">
      <Tag tone={cancellation.tone}>{cancellation.label}</Tag>

      {waitlisted && <Tag tone="waitlist">En espera · {booking.waitlist_position}</Tag>}

      {blockReason && blockReason !== "no_member" && (
        <Tag tone="norefund">{blockLabel(blockReason)}</Tag>
      )}

      {booking ? (
        <button
          type="button"
          className="btn btn--danger"
          disabled={busy}
          onClick={() => onCancel(booking)}
        >
          {busy ? "Cancelando…" : "Cancelar"}
        </button>
      ) : (
        <button
          type="button"
          className="btn btn--primary"
          disabled={busy || blockReason !== null}
          title={blockLabel(blockReason) ?? undefined}
          onClick={() => onBook(session)}
        >
          {bookLabel({ busy, full: session.full })}
        </button>
      )}
    </div>
  );
}
