import { useCallback, useState } from "react";

import { EmptyState } from "./components/EmptyState.jsx";
import { Feedback } from "./components/Feedback.jsx";
import { MemberPanel } from "./components/MemberPanel.jsx";
import { ScheduleSkeleton } from "./components/ScheduleSkeleton.jsx";
import { summarise } from "./domain/schedule.js";
import { ScheduleBoard } from "./features/ScheduleBoard.jsx";
import { StudioHeader } from "./features/StudioHeader.jsx";
import { useBookingActions } from "./hooks/useBookingActions.js";
import { useStudioData } from "./hooks/useStudioData.js";

export default function App({ api, now = new Date().toISOString(), initialMemberId = 1 }) {
  const [memberId, setMemberId] = useState(initialMemberId);
  const { classes, members, member, bookings, status, error, reload } = useStudioData(
    api,
    memberId,
  );

  const onDone = useCallback(() => reload(), [reload]);
  const { book, cancel, pendingClassId, pendingBookingId, feedback, clearFeedback } =
    useBookingActions(api, { onDone });

  const summary = summarise(classes, bookings);

  return (
    <div className="shell">
      <StudioHeader summary={summary} />

      <div className="layout">
        <main>
          {status === "loading" && <ScheduleSkeleton />}

          {status === "error" && (
            <EmptyState title="No hemos podido cargar el horario">
              <p role="alert">{error?.message}</p>
              <button type="button" className="btn btn--primary" onClick={reload}>
                Volver a intentarlo
              </button>
            </EmptyState>
          )}

          {status === "ready" && (
            <ScheduleBoard
              classes={classes}
              bookings={bookings}
              member={member}
              now={now}
              pendingClassId={pendingClassId}
              pendingBookingId={pendingBookingId}
              onBook={(session) => book(memberId, session.id)}
              onCancel={(booking) => cancel(booking.id)}
            />
          )}
        </main>

        {status === "ready" && (
          <MemberPanel
            members={members}
            member={member}
            bookings={bookings}
            classes={classes}
            pendingBookingId={pendingBookingId}
            onSelectMember={setMemberId}
            onCancel={(booking) => cancel(booking.id)}
          />
        )}
      </div>

      <Feedback feedback={feedback} onDismiss={clearFeedback} />
    </div>
  );
}
