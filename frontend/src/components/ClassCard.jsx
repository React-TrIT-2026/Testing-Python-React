import { bookingBlockReason } from "../domain/eligibility.js";
import {
  formatDuration,
  formatPrice,
  formatTime,
  levelLabel,
  statusLabel,
} from "../domain/formatting.js";

import { ClassCardActions } from "./ClassCardActions.jsx";
import { SeatMeter } from "./SeatMeter.jsx";
import { Tag } from "./Tag.jsx";

function cardClassName({ mine, full }) {
  const names = ["card"];
  if (full && !mine) names.push("card--full");
  if (mine) names.push("card--booked");
  return names.join(" ");
}

export function ClassCard({
  session,
  booking,
  member,
  now,
  onBook,
  onCancel,
  busy = false,
}) {
  const mine = Boolean(booking);
  const blockReason = mine ? null : bookingBlockReason(member, session, now);

  return (
    <article
      className={cardClassName({ mine, full: session.full })}
      aria-labelledby={`class-${session.id}-title`}
    >
      <div className="card__head">
        <h3 className="card__title" id={`class-${session.id}-title`}>
          {session.name}
        </h3>
        <div className="card__head-tags">
          <Tag tone="level">{levelLabel(session.min_level)}</Tag>
        </div>
      </div>

      <p className="card__meta">
        <span>{session.instructor}</span>
        <span aria-hidden="true">·</span>
        <span>{session.room}</span>
        <span aria-hidden="true">·</span>
        <span>{formatDuration(session.duration_min)}</span>
        <span aria-hidden="true">·</span>
        <span>{formatPrice(session.price_cents)}</span>
      </p>

      <div className="card__foot">
        <SeatMeter session={session} myStatus={booking?.status} />
        <ClassCardActions
          session={session}
          booking={booking}
          now={now}
          blockReason={blockReason}
          busy={busy}
          onBook={onBook}
          onCancel={onCancel}
        />
      </div>

      {mine && (
        <p className="visually-hidden">
          Tu reserva para {session.name} de las {formatTime(session.starts_at)} está{" "}
          {statusLabel(booking.status).toLowerCase()}
        </p>
      )}
    </article>
  );
}
