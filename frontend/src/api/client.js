export class ApiError extends Error {
  constructor(message, { status, code, cause } = {}) {
    super(message, { cause });
    this.name = "ApiError";
    this.status = status;
    this.code = code;
  }
}

const MESSAGES = {
  member_not_found: "No encontramos a este socio.",
  class_not_found: "Esta clase ya no está en el horario.",
  booking_not_found: "Esta reserva ya no existe.",
  dues_unpaid: "Tienes la cuota pendiente. Pasa por recepción para reservar.",
  payment_declined: "Tu tarjeta ha sido rechazada. Prueba con otro método de pago.",
  member_blocked: "Tienes las reservas bloqueadas por acumular ausencias.",
  level_too_low: "Esta clase pide un nivel superior al tuyo.",
  overlapping_booking: "Ya tienes otra clase a esa hora.",
  duplicate_booking: "Ya tienes esta clase reservada.",
  booking_already_cancelled: "Esta reserva ya estaba cancelada.",
  outside_booking_window: "El calendario se abre 14 días antes de la clase.",
  class_already_started: "Esta clase ya ha empezado.",
  no_credits_left: "No te quedan sesiones en el bono.",
};

export function messageForCode(code, fallback = "No hemos podido completar la operación.") {
  return MESSAGES[code] ?? fallback;
}

export function createApiClient({ baseUrl = "/api", fetchImpl } = {}) {
  const send = (url, options) => (fetchImpl ?? globalThis.fetch)(url, options);

  async function request(path, options = {}) {
    let response;
    try {
      response = await send(`${baseUrl}${path}`, {
        headers: { "Content-Type": "application/json" },
        ...options,
      });
    } catch (cause) {
      throw new ApiError("No hay conexión con el estudio. Inténtalo de nuevo.", {
        status: 0,
        cause,
      });
    }

    if (response.status === 204) return null;

    let payload = null;
    try {
      payload = await response.json();
    } catch {
      payload = null;
    }

    if (!response.ok) {
      const code = payload?.code;
      throw new ApiError(messageForCode(code, payload?.detail), {
        status: response.status,
        code,
      });
    }

    return payload;
  }

  return {
    listClasses: () => request("/classes"),
    listMembers: () => request("/members"),
    getMember: (memberId) => request(`/members/${memberId}`),
    listBookings: (memberId) => request(`/members/${memberId}/bookings`),
    book: (memberId, classId) =>
      request("/bookings", {
        method: "POST",
        body: JSON.stringify({ member_id: memberId, class_id: classId }),
      }),
    cancel: (bookingId) => request(`/bookings/${bookingId}`, { method: "DELETE" }),
  };
}
