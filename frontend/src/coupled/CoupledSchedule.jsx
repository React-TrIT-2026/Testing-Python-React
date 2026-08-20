import { useEffect, useState } from "react";

export default function CoupledSchedule({ memberId }) {
  const [classes, setClasses] = useState([]);
  const [member, setMember] = useState(null);
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    setLoading(true);
    fetch(`/api/classes`)
      .then((r) => r.json())
      .then((data) => {
        setClasses(data);
        return fetch(`/api/members/${memberId}`).then((r) => r.json());
      })
      .then((data) => {
        setMember(data);
        return fetch(`/api/members/${memberId}/bookings`).then((r) => r.json());
      })
      .then((data) => {
        setBookings(data);
        setLoading(false);
      })
      .catch(() => {
        setMessage("Algo ha ido mal");
        setLoading(false);
      });
  }, [memberId]);

  function book(classId) {
    fetch("/api/bookings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ member_id: memberId, class_id: classId }),
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.code) {
          setMessage("Error: " + data.code);
          return;
        }
        setMessage(data.waitlisted ? "En lista de espera" : "Reservado");
        return fetch(`/api/members/${memberId}/bookings`)
          .then((r) => r.json())
          .then(setBookings);
      });
  }

  if (loading) return <p>Cargando...</p>;

  return (
    <div>
      {message && <p>{message}</p>}
      <ul>
        {classes.map((session) => {
          const start = new Date(session.starts_at);
          const hours = (start.getTime() - Date.now()) / 3600000;
          const band = hours >= 12 ? "libre" : hours >= 2 ? "tardía" : "sin devolución";
          const mine = bookings.find(
            (b) =>
              b.class_id === session.id &&
              (b.status === "confirmed" || b.status === "waitlisted"),
          );
          const price = (session.price_cents / 100).toFixed(2) + " €";
          const time =
            String(start.getHours()).padStart(2, "0") +
            ":" +
            String(start.getMinutes()).padStart(2, "0");

          return (
            <li key={session.id}>
              <span>{time}</span> <strong>{session.name}</strong> <span>{price}</span>{" "}
              <span>Cancelación {band}</span>{" "}
              <span>
                {session.confirmed}/{session.capacity}
              </span>{" "}
              {mine ? (
                <span>Reservada</span>
              ) : (
                <button
                  type="button"
                  disabled={!member || !member.dues_paid}
                  onClick={() => book(session.id)}
                >
                  Reservar
                </button>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
