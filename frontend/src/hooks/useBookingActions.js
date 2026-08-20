import { useCallback, useState } from "react";

export function useBookingActions(api, { onDone } = {}) {
  const [pendingClassId, setPendingClassId] = useState(null);
  const [pendingBookingId, setPendingBookingId] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const clearFeedback = useCallback(() => setFeedback(null), []);

  const book = useCallback(
    async (memberId, classId) => {
      setPendingClassId(classId);
      setFeedback(null);
      try {
        const result = await api.book(memberId, classId);
        setFeedback({
          tone: "ok",
          message: result.waitlisted
            ? `Estás en la lista de espera, puesto ${result.position}.`
            : "Plaza confirmada. Nos vemos en la sala.",
        });
        await onDone?.();
        return result;
      } catch (caught) {
        setFeedback({ tone: "error", message: caught.message });
        return null;
      } finally {
        setPendingClassId(null);
      }
    },
    [api, onDone],
  );

  const cancel = useCallback(
    async (bookingId) => {
      setPendingBookingId(bookingId);
      setFeedback(null);
      try {
        const result = await api.cancel(bookingId);
        setFeedback({ tone: "ok", message: messageForBand(result) });
        await onDone?.();
        return result;
      } catch (caught) {
        setFeedback({ tone: "error", message: caught.message });
        return null;
      } finally {
        setPendingBookingId(null);
      }
    },
    [api, onDone],
  );

  return { book, cancel, pendingClassId, pendingBookingId, feedback, clearFeedback };
}

function messageForBand(result) {
  if (result.band === "free") return "Reserva cancelada sin coste.";
  if (result.band === "late")
    return "Reserva cancelada. Se te descuenta 1 sesión por avisar tarde.";
  if (result.band === "waitlist") return "Te hemos sacado de la lista de espera.";
  return "Reserva cancelada fuera de plazo: pierdes la sesión.";
}
